from django.urls import path,include
from . import views
from admins import urls

urlpatterns = [
    path('',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    # path('admin/',include('admin.urls')),
    path('dashboard/',views.dash,name="dash"),
    path('logout/',views.user_logout,name="logout"),
    path('feestructure/',views.feestru,name='feestru'),
    path('update-prof/<int:pk>/',views.updateprof,name='update-prof'),
]
