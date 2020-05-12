from django.contrib import admin
from django.urls import path

from . import views, leave_manager_views

urlpatterns = [
    # User Access
    path('leaves/', views.leaves_view, name='leaves'),
    path('archive-leaves/', views.archive_leaves_view, name='archive_leaves'),
    path('create-leave/', views.create_leave, name='create_leave'),
    path('<int:id>/delete-leave/', views.delete_leave, name='delete_leave'),
    path('<int:id>/archive-leave/', views.archive_leave, name='archive_leave'),
    path('<int:id>/delete-archive-leave', views.delete_archive_leave, name='delete_archive_leave'),
    
    # Manager Access
    path('manage-leaves/', leave_manager_views.manager_leaves_view, name='manager_leaves'),
    path('leaves-bar-chart/', leave_manager_views.total_leaves_monthly_bar_chart, name='leaves_bar_chart'),
    path('<int:id>/leave-detail/',leave_manager_views.manager_leaves_detail, name='leave_detail'),
]
