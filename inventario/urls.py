from django.urls import path
from .views import UserLoginView

app_name = 'inventario'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
]