import datetime

from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets, permissions, authentication, mixins, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import Todo, TodoFolders
from . import serializers as sz
from .exceptions import BadRequest


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='completed', description="Filter complete/incomplete", type=bool),
        OpenApiParameter(name='until', description="End date. Results with no end date will be hidden.",
                         type=OpenApiTypes.DATETIME),
    ])
)
@extend_schema(tags=["Todo"])
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = sz.TodoRetrieveSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    model = Todo

    def get_serializer_class(self):
        if self.action == 'create':
            return sz.TodoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return sz.TodoUpdateSerializer

        return sz.TodoRetrieveSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        try:
            query = self.request.query_params
            filter_query = Q(user=self.request.user)
            if "completed" in query:
                raw = query["completed"].capitalize()
                state = True if raw == "True" else False
                filter_query &= Q(is_completed=state)
            if "end_date" in query:
                date = datetime.datetime.fromisoformat(query["end_date"])
                filter_query &= Q(until__lt=date + datetime.timedelta(days=1),
                                  until__gte=date)
            return self.queryset.filter(filter_query)
        except ValueError as ex:
            if "Invalid isoformat string" in str(ex):
                raise BadRequest("Bad datetime format", code=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=serializer_class,
        description="Title is required. Other fields can be provided optionally."
    )
    def create(self, request, *args, **kwargs):
        serializer: sz.TodoCreateSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            folder = None
            slug = serializer.validated_data.pop("slug", None)
            if slug:
                folder = get_object_or_404(TodoFolders, slug=slug, user_id=request.user.id)

            instance = serializer.create(serializer.validated_data)

            if folder:
                folder.todo_list.add(instance)

            serializer = self.serializer_class(instance)
            # headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=sz.TodoChangeStateSerializer,
                   parameters=[OpenApiParameter(name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                                                description="ID")])
    @action(detail=False, methods=['patch'], url_path=r'state/(?P<id>[^/]+)')
    def change_state(self, request: Request, id):
        """Change state of to-do"""
        state = request.data.get("state")
        if state is None or (bool(state) not in [True, False]):
            return Response({"detail": "Param <state> should be valid boolean"}, status=status.HTTP_400_BAD_REQUEST)
        state = bool(state)
        instance: Todo = get_object_or_404(Todo, pk=id, user=request.user)
        instance.change_state(state)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["Folders"])
class FoldersViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = TodoFolders.objects.all()
    serializer_class = sz.FolderRetrieveSerializer
    lookup_field = "slug"
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        query = self.request.query_params.keys()
        filter_query = Q(user=self.request.user)

        return self.queryset.filter(filter_query)


@extend_schema(tags=["Folders"])
class FolderManageViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          GenericViewSet):
    queryset = TodoFolders.objects.all()
    serializer_class = sz.FolderSerializer
    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "slug"
    http_method_names = ["post", "put", "patch", "delete"]

    def get_queryset(self):
        # query = self.request.query_params.keys()
        filter_query = Q(user=self.request.user)

        return self.queryset.filter(filter_query)

    @extend_schema(request=sz.FolderSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = TodoFolders.objects.create(user_id=request.user.id,
                                                      folder_title=serializer.validated_data.get("folder_title"))
                if serializer.validated_data.get("todo_list"):
                    filtered_todos = [todo for todo in serializer.validated_data.get("todo_list")
                                      if todo.user.id == request.user.id]
                    instance.todo_list.add(*filtered_todos)
                serializer = self.serializer_class(instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"detail": "Folder with this name already exists"}, status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id="api_folder_todo_add", methods=["PUT"])
    @extend_schema(operation_id="api_folder_todo_remove", methods=["DELETE"])
    @extend_schema(request=None, responses=sz.FolderRetrieveSerializer,
                   parameters=[OpenApiParameter(name="todo_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                                                description="Todo ID")])
    @action(detail=True, methods=['put', "delete"],
            url_path=r'(?P<todo_id>\d+)')
    def manage_todo_in_folder(self, request, slug, todo_id):
        if request.method == "PUT":
            instance: TodoFolders = self.get_object()
            todo = get_object_or_404(Todo, user_id=request.user.id, pk=todo_id)
            instance.todo_list.add(todo)
            return Response(sz.FolderRetrieveSerializer(instance).data)
        elif request.method == "DELETE":
            todo = get_object_or_404(Todo, user_id=request.user.id, pk=todo_id)
            instance: TodoFolders = self.get_object()
            instance.todo_list.remove(todo)
            return Response(status=status.HTTP_204_NO_CONTENT)
