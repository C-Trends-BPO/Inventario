from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from ..models import LoteBipagem, Caixa, Bipagem
from ..forms import BipagemForm
from django.core.paginator import Paginator

def bipagem(request, lote_id, caixa_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    caixa = get_object_or_404(Caixa, id=caixa_id, lote=lote)

    if request.method == 'POST':
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
    paginator = Paginator(bipagens_da_caixa, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    caixa_bloqueada = caixa.status in ['Finalizada']

    context = {
        'lote': lote,
        'caixa': caixa,
        'form': form,
        'caixas': bipagens_da_caixa, 
        'caixa_bloqueada': caixa_bloqueada,
        'page_obj': page_obj,
    }

    return render(request, 'inventario/bipagem.html', context)
