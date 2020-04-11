from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('create-leave/', views.create_leave, name='create_leave'),
    path('leaves/', views.leaves_view, name='leaves'),
]
