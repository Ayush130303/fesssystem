from django.urls import path,include
from . import views
from admins import urls

urlpatterns = [
    path('',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    # path('admin/',include('admin.urls')),
    path('dashboard/',views.stu_dash,name="stu_dash"),
]
