from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ..models import LoteBipagem, Caixa
from ..forms import CaixaForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required(login_url='inventario:login')
def lote(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)

    # Impede ações POST para o grupo de visualização
    if request.method == 'POST' and request.user.groups.filter(name='Visualizador Master').exists():
        return HttpResponseForbidden("Você não tem permissão para modificar esse lote.")

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

    caixas_list = Caixa.objects.filter(lote=lote).order_by('-id')
    paginator = Paginator(caixas_list, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    caixas_abertas = lote.caixas.filter(status='Iniciada').exists()
    is_visualizador_master = request.user.groups.filter(name='INV_VISUALIZADOR_MASTER').exists()
    lote_bloqueado = lote.status in ['fechado', 'cancelado']

    context = {
        'form': form,
        'page_obj': page_obj,      
        'lote': lote,
        'caixas_abertas': caixas_abertas,
        'lote_bloqueado': lote_bloqueado,
        'is_visualizador_master': is_visualizador_master,
    }

    return render(request, 'inventario/lote.html', context)