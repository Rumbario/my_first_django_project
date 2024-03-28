from django.urls import path
from .views import UserLoginView, UserRegisterView, user_logout, UserSettingsView, change_password

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),
    path('change_password/', change_password, name='change_password'),

]