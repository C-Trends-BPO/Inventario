# views.py
from django.shortcuts import redirect, get_object_or_404,render

from inventario.forms.caixa_forms import CaixaForm
from ..models import LoteBipagem, Caixa

def iniciar_caixa_redirect(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)

    if request.method == 'POST':
        nova_caixa = Caixa.objects.create(
            lote=lote,
            identificador=f"Caixa {lote.caixas.count() + 1}",
            nr_caixa = lote.caixas.count() + 1
        )
        return redirect('inventario:lote', lote_id=lote.id) 

    else:
        form = CaixaForm()
        caixas = Caixa.objects.filter(lote=lote)
        context = {
            'form': form,
            'caixas': caixas,
            'lote': lote,
        }
        return render(request, 'inventario/lote.html', context)