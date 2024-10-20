from django.urls import path
from accounts.views import *
urlpatterns = [
    path('user_login',user_login,name="user_login"),
    path('user_register',user_register,name="user_register"),
    path('user_logout',user_logout,name="user_logout"),
]
