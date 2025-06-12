from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from inventario.forms.caixa_forms import CaixaForm
from ..models import LoteBipagem, Caixa

def iniciar_caixa_redirect(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    nova_caixa = Caixa.objects.create(
        lote=lote,
        nr_caixa=str(lote.caixas.count() + 1),
        identificador=f"Caixa {lote.caixas.count() + 1}",
    )

    return redirect('inventario:caixa', lote_id=lote.id, caixa_id=nova_caixa.id)