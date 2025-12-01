from django.urls import path
from user_accounts.views import *

urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('login/', user_login,name='login'),
    path('logout/', user_logout, name='logout'),
    path('user-profile/<int:id>/', user_profile, name='profile'),
    path('user-change-password/', user_change_password, name='change-password'),
]
