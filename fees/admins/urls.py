from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dash, name='dash'),
    path('admin/announcements/', views.view_announcements, name='view-announcements'),
    path('admin/fee-structure/', views.fee_structure, name='fee-structure'),
    path('admin/fee-submissions/', views.fee_submissions, name='fee-submissions'),
    path('admin/students/', views.view_students, name='view-students'),
    path('admin/logout/', views.admin_logout, name='ad_logout'),
]
