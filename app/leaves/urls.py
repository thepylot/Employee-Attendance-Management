from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('leaves/', views.leaves_view, name='leaves'),
    path('create-leave/', views.create_leave, name='create_leave'),
    path('<int:id>/delete-leave/', views.delete_leave, name='delete_leave'),
]
