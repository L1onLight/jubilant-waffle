from django.urls import path

from . import views

urlpatterns = [
    path('restore/', views.restore_mail, name="restore_password"),
    path('check/', views.check_code, name="check_code"),
]
