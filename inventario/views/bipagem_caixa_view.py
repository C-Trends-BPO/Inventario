from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from ..models import LoteBipagem, Caixa, Bipagem
from ..forms import BipagemForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
@login_required(login_url='inventario:login')
def bipagem(request, lote_id, caixa_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    caixa = get_object_or_404(Caixa, id=caixa_id, lote=lote)

    # Verifica se é usuário visualizador
    is_visualizador_master = request.user.groups.filter(name='INV_VISUALIZADOR_MASTER').exists()

    if request.method == 'POST' and is_visualizador_master:
        return HttpResponseForbidden("Você não tem permissão para bipar seriais.")

    if request.method == 'POST':
        form = BipagemForm(request.POST)
        serial = request.POST.get('serial', '').strip()

        if Bipagem.objects.filter(id_caixa=caixa).count() >= 50:
            form.add_error(None, "Esta caixa já possui o limite de 50 bipagens.")
        elif form.is_valid() and serial:
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
    mensagem = {'mostrar': True, 'encerrar': True}

    caixa_bloqueada = caixa.status in ['Finalizada']
    if caixa_bloqueada:
        mensagem = {'mensagem': 'Esta caixa está bloqueada e não pode ser editada.', 'voltar': True}
    elif bipagens_da_caixa.count() >= 50:
        mensagem = {'mensagem': 'Esta caixa já possui o limite de 50 bipagens.', 'encerrar': True}

    context = {
        'lote': lote,
        'caixa': caixa,
        'form': form,
        'caixas': bipagens_da_caixa,
        'page_obj': page_obj,
        'mensagem': mensagem,
        'is_visualizador_master': is_visualizador_master,  # 👈 AQUI está a correção
    }

    return render(request, 'inventario/bipagem.html', context)
