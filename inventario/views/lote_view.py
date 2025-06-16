from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ..models import LoteBipagem, Caixa
from ..forms import CaixaForm

def lote(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    
    if request.method == 'POST':
        if 'encerrar_caixa' in request.POST:
            caixa_aberta = lote.caixas.filter(status='Iniciada').last()
            if caixa_aberta:
                caixa_aberta.status = 'Finalizada'
                caixa_aberta.save()
            return redirect('inventario:lote', lote_id=lote.id)
        
        form = CaixaForm(request.POST)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.lote = lote
            caixa.nr_caixa = lote.caixas.count() + 1
            caixa.save()
            return redirect('inventario:lote', lote_id=lote.id)
    else:
        form = CaixaForm()

    caixas = Caixa.objects.filter(lote=lote).order_by('-id')
    caixas_abertas = lote.caixas.filter(status='Iniciada').exists()
    lote_bloqueado = lote.status in ['fechado', 'cancelado']

    context = {
        'form': form,
        'caixas': caixas,
        'lote': lote,
        'caixas_abertas': caixas_abertas,
        'lote_bloqueado': lote_bloqueado
    }

    return render(request, 'inventario/lote.html', context)