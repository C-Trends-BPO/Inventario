from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ..models import LoteBipagem
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def index(request):
    if request.method == 'POST' and 'fechar_lote_id' in request.POST:
        lote_id = request.POST.get('fechar_lote_id')
        lote = get_object_or_404(LoteBipagem, id=lote_id)
        lote.status = 'Aguardando Validação'
        lote.save()
        return redirect('inventario:index')

    lotes_list = LoteBipagem.objects.all().order_by('-criado_em')
    paginator = Paginator(lotes_list, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventario/index.html', {
        'lotes': page_obj.object_list,
        'page_obj': page_obj
    })