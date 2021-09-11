"""
@Author: Guangzheng Hu
Student ID: 692277

Description: Test file
"""
from django.urls import path
from hello import views

urlpatterns = [
    path("test/<int:a>/<int:b>/<int:c>", views.home, name="home"),
    path("hello/<name>", views.hello_there, name="hello_there"),
]