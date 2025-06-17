from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
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

    busca = request.GET.get('q', '')

    lotes_list = LoteBipagem.objects.all().order_by('-criado_em')
    if busca:
        lotes_list = lotes_list.filter(
            Q(id__icontains=busca) |
            Q(status__icontains=busca) |  
            Q(user_created__username__icontains=busca)
        )

    paginator = Paginator(lotes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventario/index.html', {
        'lotes': page_obj.object_list,
        'page_obj': page_obj
    })


def listar_lotes(request):
    busca = request.GET.get('q', '')
    lotes = LoteBipagem.objects.all()

    if busca:
        lotes = lotes.filter(
            Q(id__icontains=busca) |
            Q(status__icontains=busca) |
            Q(user_created__username__icontains=busca)
        )

    paginator = Paginator(lotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventario/listar_lotes.html', {
        'lotes': page_obj.object_list,
        'page_obj': page_obj,
    })