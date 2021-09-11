"""
@Author: Guangzheng Hu
Student ID: 692277

Description: This file contains URL API defined with the frontend.
"""
from django.urls import path
from api import views

urlpatterns = [
    path("api/test/<int:n>", views.get_n_tweet, name="get_n_tweet"),
    path("api/death/<str:month>", views.get_death_number, name="get_death_number"),
    path("api/employment", views.get_employment, name="get_employment"),
    path("api/tweet/top/<str:mode>/<int:n>/<str:timeS>/<str:timeE>", views.get_top, name="get_top"),
    path("api/cases", views.get_cases, name="get_cases"),
    path("api/language", views.get_lang, name="get_lang"),
    path("api/area/info", views.get_areaInfo, name="get_areaInfo"),
    path("api/area/age", views.get_areaAge, name="get_areaAge"),
    path("api/area/tweet", views.get_areaTweet, name="get_areaTweet"),
    path("api/language/heatmap/<str:lang>", views.get_langHeat, name="get_langHeat"),
]