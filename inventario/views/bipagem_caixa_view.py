from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from ..models import LoteBipagem, Caixa, Bipagem
from ..forms import BipagemForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required(login_url='inventario:login')
def bipagem(request, lote_id, caixa_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    caixa = get_object_or_404(Caixa, id=caixa_id, lote=lote)

    limite_por_pa = getattr(lote.group_user.informacoes, 'limite', 50)
    is_visualizador_master = request.user.groups.filter(name='INV_PA_VISUALIZADOR_MASTER').exists()

    exibir_consultar = True

    if request.method == 'POST' and is_visualizador_master:
        return HttpResponseForbidden("Você não tem permissão para bipar seriais.")

    if request.method == 'POST':
        form = BipagemForm(request.POST)
        serial = form.data.get('serial', '').strip()

        # 🔍 CONSULTAR DADOS AUTOMATICAMENTE
        if 'buscar_dados' in request.POST and form.is_valid():
            from ..models import InventarioDadosImportados
            serial = form.cleaned_data.get('serial', '').strip()
            print(f"🔍 Buscando serial: '{serial}'")
            dados = InventarioDadosImportados.objects.filter(serial__iexact=serial).first()

            if dados:
                print("✅ Serial encontrado:")
                print("📦 Modelo:", dados.modelo)
                print("📦 Patrimônio:", dados.serial_fabricante)

                form = BipagemForm(initial={
                    'serial': serial,
                    'modelo': dados.modelo,
                    'patrimonio': dados.serial_fabricante,
                    'estado': form.cleaned_data.get('estado', '')
                })
                messages.info(request, "ℹ️ Dados preenchidos automaticamente.")
                exibir_consultar = False
            else:
                print("❌ Serial não encontrado no banco.")
                messages.warning(request, f"⚠️ Serial '{serial}' não encontrado.")

        qtd_seriais = Bipagem.objects.filter(id_caixa=caixa).count()
        if qtd_seriais >= limite_por_pa and qtd_seriais != 0:
            form.add_error(None, f"Esta caixa já atingiu o limite de {limite_por_pa} bipagens definido para esta PA.")
            messages.warning(request, f"⚠️ Esta caixa já possui o limite de {limite_por_pa} bipagens.")

        if 'encerrar_caixa' in request.POST and qtd_seriais != 0:
            caixa_aberta = lote.caixas.filter(status='Iniciada').last()
            if caixa_aberta:
                caixa_aberta.status = 'Finalizada'
                caixa_aberta.save()
            request.session.pop('modelo_bipagem', None)
            return redirect('inventario:lote', lote_id=lote.id)

        elif 'encerrar_caixa' in request.POST and qtd_seriais == 0:
            form.add_error(None, "Nenhum serial foi fornecido.")
            messages.warning(request, "⚠️ Nenhum serial foi fornecido.")

        elif form.is_valid() and serial:
            if not form.cleaned_data.get('estado'):
                form.add_error('estado', "Este campo é obrigatório.")
                messages.warning(request, "⚠️ Preencha o campo Estado antes de inserir.")
            else:
                bipagens_mesma_pa = Bipagem.objects.filter(group_user=lote.group_user, nrserie=serial)
                serial_em_lote_ativo = bipagens_mesma_pa.exclude(id_lote__status='cancelado').exists()

                if serial_em_lote_ativo:
                    messages.error(request, f"❌ O serial '{serial}' já foi inserido nesta PA.", extra_tags='serial_repetido')
                else:
                    Bipagem.objects.create(
                        id_caixa=caixa,
                        id_lote=lote,
                        group_user=lote.group_user,
                        nrserie=serial,
                        unidade=caixa.bipagem.count() + 1,
                        estado=form.cleaned_data['estado'],
                        modelo=form.cleaned_data['modelo'],
                        patrimonio=form.cleaned_data['patrimonio']
                    )
                    request.session['modelo_bipagem'] = form.cleaned_data['modelo']
                    messages.success(request, "✅ Serial bipado com sucesso!")
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
        messages.error(request, "❌ Esta caixa está bloqueada.")
    elif bipagens_da_caixa.count() >= limite_por_pa:
        mensagem = {'mensagem': f'Esta caixa já possui o limite de {limite_por_pa} bipagens.', 'encerrar': True}
        messages.warning(request, f"⚠️ Esta caixa já possui o limite de {limite_por_pa} bipagens.")

    context = {
        'lote': lote,
        'caixa': caixa,
        'form': form,
        'caixas': bipagens_da_caixa,
        'page_obj': page_obj,
        'mensagem': mensagem,
        'is_visualizador_master': is_visualizador_master,
        'exibir_consultar': exibir_consultar,
    }

    return render(request, 'inventario/bipagem.html', context)
