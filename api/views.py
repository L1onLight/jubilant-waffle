from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(["GET"])
def get_routes(request):
    """Returns rest_framework response with paths for api"""

    routes = [
        'GET /api',
        # 'GET',
        # 'GET',
    ]

    return Response(routes)
