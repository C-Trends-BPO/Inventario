from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from ..models import LoteBipagem, Caixa, Bipagem
from ..forms import BipagemForm

def bipagem(request, lote_id, caixa_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    caixa = get_object_or_404(Caixa, id=caixa_id, lote=lote)

    if request.method == 'POST':
        if 'encerrar_caixa' in request.POST:
            return redirect(reverse('inventario:iniciar_caixa', args=[lote.id]))

        form = BipagemForm(request.POST)
        serial = request.POST.get('serial', '').strip()
            
        if form.is_valid() and serial:
            Bipagem.objects.create(
                id_caixa=caixa,
                id_lote=lote,
                nrserie=serial,
                unidade=caixa.bipagem.count() + 1,
                modelo=form.cleaned_data['modelo'],
                patrimonio=form.cleaned_data['patrimonio']
            )

            return redirect(reverse('inventario:caixa', args=[lote.id, caixa.id]))

    else:
        form = BipagemForm()

    bipagens_da_caixa = Bipagem.objects.filter(id_caixa=caixa).order_by('-id')

    context = {
        'lote': lote,
        'caixa': caixa,
        'form': form,
        'caixas': bipagens_da_caixa, 
    }

    return render(request, 'inventario/bipagem.html', context)
