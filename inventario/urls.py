from .views import UserLoginView
from .views import RegisterView
from django.urls import path
from .views import index, logout_confirm_view, logout_view

app_name = 'inventario'

urlpatterns = [
    path('', index, name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_confirm_view, name='logout_confirm'),
    path('logout/confirm/', logout_view, name='logout'),
]