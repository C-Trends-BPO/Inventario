from django.shortcuts import render, get_object_or_404
from ..models import LoteBipagem, Caixa
from ..forms import BipagemForm

def bipagem(request, lote_id, caixa_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    caixa = get_object_or_404(Caixa, nr_caixa=caixa_id, lote=lote)

    form = BipagemForm()

    context = {
        'lote': lote,
        'caixa': caixa,
        'form': form,
    }

    return render(request, 'inventario/bipagem.html', context)
