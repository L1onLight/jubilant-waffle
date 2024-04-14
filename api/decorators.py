from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def login_required_api(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Replace 'logout' with the appropriate URL name or path
            return Response({'message': "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)

    return wrapper
