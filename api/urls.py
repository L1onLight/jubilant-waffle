from django.urls import path, include
from drf_spectacular.utils import extend_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from . import views

# app_name = "api"

router = DefaultRouter()
router.register("todo", views.TodoViewSet)
router.register("folder/retrieve", views.FoldersViewSet, basename="folder_retrieve")
router.register("folder/manage", views.FolderManageViewSet, basename="folder_manage")
urlpatterns = [
    path('', include(router.urls)),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# print(router.urls)
