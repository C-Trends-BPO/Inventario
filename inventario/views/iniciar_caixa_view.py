from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from inventario.forms.caixa_forms import CaixaForm
from ..models import LoteBipagem, Caixa

def iniciar_caixa_redirect(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)

    if request.method == 'POST':
        caixas = Caixa.objects.filter(lote=lote)
        
        nova_caixa = Caixa.objects.create(
            lote=lote,
            identificador=f"Caixa {caixas.count() + 1}",
            nr_caixa=caixas.count() + 1
        )

        return redirect(reverse('inventario:caixa', kwargs={
            'lote_id': lote.id,
            'caixa_id': nova_caixa.nr_caixa
        }))

    else:
        form = CaixaForm()
        caixas = Caixa.objects.filter(lote=lote)
        context = {
            'form': form,
            'caixas': caixas,
            'lote': lote,
        }
        return render(request, 'inventario/lote.html', context)
