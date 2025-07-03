from .base_view import index
from .login_view import UserLoginView
from .register_view import RegisterView
from .logout_view import logout_view
from .logout_confirm_view import logout_confirm_view
from .criar_lote_view import criar_lote_view
from .lote_view import lote
from .iniciar_caixa_view import iniciar_caixa_redirect
from .bipagem_caixa_view import bipagem, editar_serial, excluir_serial
from .validacao_view import validar_lote_view, validar_serial, finalizar_lote_view
from .acompanhamento_view import acompanhamento_dash
from .download_extracao_pdf import download_extracao_pdf