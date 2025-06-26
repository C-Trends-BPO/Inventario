from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import LoteBipagem, Bipagem, Caixa
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required(login_url='inventario:login')
def index(request):
    is_visualizador_master = request.user.groups.filter(name='INV_PA_VISUALIZADOR_MASTER').exists()

    if request.method == 'POST' and is_visualizador_master:
        return HttpResponseForbidden("Você não tem permissão para bipar seriais.")
    
    if request.method == 'POST' and 'fechar_lote_id' in request.POST:
        lote_id = request.POST.get('fechar_lote_id')
        lote = get_object_or_404(LoteBipagem, id=lote_id)

        if not Bipagem.objects.filter(id_caixa__lote=lote).exists():
            messages.error(request, "Não é possível finalizar o lote sem nenhum serial bipado.")

        else:
            lote.status = 'Aguardando Validação'
            lote.save()
            return redirect('inventario:validar_lote')

    busca = request.GET.get('q', '')

    user_groups = request.user.groups.all()
    is_visualizador_master = request.user.groups.filter(name='INV_PA_VISUALIZADOR_MASTER').exists()

    if is_visualizador_master:
        lotes_list = LoteBipagem.objects.all().order_by('-criado_em')
    else:
        lotes_list = LoteBipagem.objects.filter(group_user__in=user_groups).order_by('-criado_em')
    
    if busca:
        try:
            busca_id = int(busca)
            filtro_id = Q(id=busca_id)
        except ValueError:
            filtro_id = Q()

        lotes_list = lotes_list.filter(
            filtro_id |
            Q(status__icontains=busca) |
            Q(user_created__username__icontains=busca)
        )

    paginator = Paginator(lotes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventario/index.html', {
        'lotes': page_obj.object_list,
        'page_obj': page_obj,
        'is_visualizador_master': is_visualizador_master, 
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