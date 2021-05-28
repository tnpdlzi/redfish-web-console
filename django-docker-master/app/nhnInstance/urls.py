from django.urls import path

from nhnInstance import views

urlpatterns = [
    path('api/instance', views.instance_list),
]