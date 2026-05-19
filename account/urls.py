from django.urls import path

from .views import login_account_view, logout_view, register_view

urlpatterns = [
    path('login/', login_account_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
