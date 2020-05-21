from django.urls import path

from users.views import authenticate_user


urlpatterns = [
    path('api/auth/login', authenticate_user),
]
