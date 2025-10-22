app_name = 'ragaspace'

from django.urls import path

from .views import EmailLoginView, LogoutUserView, dashboard, register

urlpatterns = [
    path('', register, name='register'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
