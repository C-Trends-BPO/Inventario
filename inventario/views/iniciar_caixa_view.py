from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from inventario.forms.caixa_forms import CaixaForm
from ..models import LoteBipagem, Caixa
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required(login_url='inventario:login')
def iniciar_caixa_redirect(request, lote_id):
    # Bloqueia a criação da caixa para usuários do grupo de visualização
    if request.user.groups.filter(name='INV_VISUALIZADOR_MASTER').exists():
        return HttpResponseForbidden("Você não tem permissão para iniciar caixas.")

    lote = get_object_or_404(LoteBipagem, id=lote_id)

    nova_caixa = Caixa.objects.create(
        lote=lote,
        nr_caixa=str(lote.caixas.count() + 1),
        identificador=f"Caixa {lote.caixas.count() + 1}",
    )

    return redirect('inventario:caixa', lote_id=lote.id, caixa_id=nova_caixa.id)