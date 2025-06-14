from .views import UserLoginView
from .views import RegisterView
from django.urls import path
from .views import index, logout_confirm_view, logout_view, criar_lote_view, lote, \
iniciar_caixa_redirect, bipagem


app_name = 'inventario'

urlpatterns = [
    path('', index, name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_confirm_view, name='logout_confirm'),
    path('logout/confirm/', logout_view, name='logout'),
    path('lote/criar/', criar_lote_view, name='criar_lote'),
    path('lote/<int:lote_id>/', lote, name='lote'),
    path('lote/<int:lote_id>/caixas/', iniciar_caixa_redirect, name='iniciar_caixa'),
    path('lote/<int:lote_id>/caixas/<int:caixa_id>/', bipagem, name='caixa'),
]