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

    mensagem_ferramenta = request.session.get('mensagem_ferramenta', None)
    exibir_consultar = True
    modelo_autocompletado = False

    if request.method == 'POST' and is_visualizador_master:
        return HttpResponseForbidden("Você não tem permissão para bipar seriais.")

    if request.method == 'POST':
        form = BipagemForm(request.POST)
        serial = form.data.get('serial', '').strip()

        if 'buscar_dados' in request.POST and form.is_valid():
            from ..models import InventarioDadosImportados
            serial = form.cleaned_data.get('serial', '').strip()
            dados = InventarioDadosImportados.objects.filter(serial__iexact=serial).first()

            if dados:
                modelo_autocompletado = True
                mensagem_ferramenta = dados.mensagem_ferramenta_inv
                request.session['mensagem_ferramenta'] = mensagem_ferramenta
                request.session['modelo_autocompletado'] = True
                exibir_consultar = False

                serial_ja_bipado = Bipagem.objects.filter(nrserie=serial).exists()
                observacao = "Duplicidade" if serial_ja_bipado else ""

                Bipagem.objects.create(
                    id_caixa=caixa,
                    id_lote=lote,
                    group_user=lote.group_user,
                    nrserie=serial,
                    unidade=caixa.bipagem.count() + 1,
                    estado=form.cleaned_data['estado'],
                    modelo=dados.modelo,
                    observacao=observacao,
                )
                request.session['estado_bipagem'] = form.cleaned_data['estado']
                messages.success(request, "✅ Serial inserido com sucesso!")
                return redirect(reverse('inventario:caixa', args=[lote.id, caixa.id]))

            else:
                form = BipagemForm(initial={
                    'serial': serial,
                    'modelo': '',
                    'estado': form.cleaned_data.get('estado', '')
                })
                exibir_consultar = False
                modelo_autocompletado = False
                request.session.pop('modelo_autocompletado', None)
                request.session.pop('mensagem_ferramenta', None)
                messages.warning(request, f"⚠️ Serial '{serial}' não encontrado.")

        elif 'encerrar_caixa' in request.POST:
            qtd_seriais = Bipagem.objects.filter(id_caixa=caixa).count()
            if qtd_seriais == 0:
                form.add_error(None, "Nenhum serial foi fornecido.")
                messages.warning(request, "⚠️ Nenhum serial foi fornecido.")
            else:
                caixa_aberta = lote.caixas.filter(status='Iniciada').last()
                if caixa_aberta:
                    caixa_aberta.status = 'Finalizada'
                    caixa_aberta.save()
                request.session.pop('modelo_bipagem', None)
                return redirect('inventario:lote', lote_id=lote.id)

        elif form.is_valid() and serial:
            if not form.cleaned_data.get('estado'):
                messages.warning(request, "⚠️ Preencha o campo Estado antes de inserir.")
            elif not form.cleaned_data.get('modelo'):
                messages.warning(request, "⚠️ Preencha o campo Modelo antes de inserir.")
            else:
                serial_ja_bipado = Bipagem.objects.filter(nrserie=serial).exists()
                observacao = "Duplicidade" if serial_ja_bipado else ""

                Bipagem.objects.create(
                    id_caixa=caixa,
                    id_lote=lote,
                    group_user=lote.group_user,
                    nrserie=serial,
                    unidade=caixa.bipagem.count() + 1,
                    estado=form.cleaned_data['estado'],
                    modelo=form.cleaned_data['modelo'],
                    observacao=observacao,
                )
                request.session['estado_bipagem'] = form.cleaned_data['estado']
                messages.success(request, "✅ Serial inserido com sucesso!")
                return redirect(reverse('inventario:caixa', args=[lote.id, caixa.id]))

    else:
        form = BipagemForm(initial={
            'estado': request.session.get('estado_bipagem', ''),
            'modelo': ''
        })

    modelo_autocompletado = request.session.pop('modelo_autocompletado', False)

    bipagens_da_caixa = Bipagem.objects.filter(id_caixa=caixa).order_by('-id')
    paginator = Paginator(bipagens_da_caixa, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    mensagem = {'mostrar': True, 'encerrar': True}

    if caixa.status == 'Finalizada':
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
        'modelo_autocompletado': modelo_autocompletado,
        'mensagem_ferramenta': mensagem_ferramenta,
    }

    return render(request, 'inventario/bipagem.html', context)
