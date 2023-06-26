from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.home, name='home'),
    path('login/<str:fool>', views.log_in, name='login2'),
    path('login/', views.log_in, name='login'),
    path('restore-password/', views.restore_mail, name='p_restore'),
    path('logout/', views.log_out, name='logout'),
    path('folder/<folder_name>/', views.folder_page, name='folder_page'),
    path('createExampleUser/', views.create_example_user, name='example_user'),
]
