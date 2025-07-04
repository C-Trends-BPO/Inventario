from .views import UserLoginView
from .views import RegisterView
from django.urls import path
from .views import index, logout_confirm_view, logout_view, criar_lote_view, lote, \
iniciar_caixa_redirect, bipagem, validar_lote_view, validar_serial, finalizar_lote_view, \
acompanhamento_dash, download_extracao_pdf, editar_serial, excluir_serial, relatorios_view, \
download_extracao_csv


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
    path('lote/<int:lote_id>/validar/', validar_lote_view, name='validar_lote'),
    path('lote/<int:lote_id>/validar/serial/', validar_serial, name='validar_serial'),
    path('lote/<int:lote_id>/fechar/', finalizar_lote_view, name='fechar_lote'),
    path('acompanhamento/', acompanhamento_dash, name='acompanhamento'),
    path('download-extracao/', download_extracao_pdf, name='download_extracao'),
    path('serial/<int:serial_id>/editar/', editar_serial, name='editar_serial'),
    path('serial/<int:serial_id>/excluir/', excluir_serial, name='excluir_serial'),
    path('relatorios/', relatorios_view, name='relatorios'),
    path('extracao/', download_extracao_csv, name='download_extracao_csv'),
]