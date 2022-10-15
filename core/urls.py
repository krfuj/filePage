from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('homepage', views.homepage, name='homepage'),
    path('upload', views.upload, name='upload'),
    path('delete_file', views.delete_file, name='delete_file'),
    #path('edit_file/<str:id>/edit/', views.editFile, name='edit_file'),
    path('download', views.download, name='download'),
    path('signout', views.signout, name='signout'),
]