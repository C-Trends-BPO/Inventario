from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Count
from inventario.models import LoteBipagem, Bipagem
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@login_required(login_url='inventario:login')
def download_extracao_pdf(request):
    user = request.user
    responsavel = user.get_full_name() or user.username
    grupos = user.groups.values_list('name', flat=True)
    pa_param = request.GET.get('pa')  # <-- Aqui pegamos a PA selecionada na URL

    is_admin_total = 'INV_PA_GER_TOTAL' in grupos

    # Caso seja um admin e tenha selecionado uma PA:
    if is_admin_total and pa_param:
        lotes = LoteBipagem.objects.filter(group_user__name=pa_param)
        total_lotes = lotes.count()
        total_caixas = Bipagem.objects.filter(id_caixa__lote__group_user__name=pa_param).values('id_caixa').distinct().count()
        total_seriais = Bipagem.objects.filter(id_caixa__lote__group_user__name=pa_param).count()

        nome_pa = pa_param
        grupo = Group.objects.filter(name=pa_param).first()
        endereco_pa = getattr(grupo.informacoes, "endereco", "Não informado") if grupo else "Não informado"

    elif is_admin_total and not pa_param:
        # Acesso geral para todos
        lotes = LoteBipagem.objects.all()
        total_lotes = lotes.count()
        total_caixas = Bipagem.objects.values('id_caixa').distinct().count()
        total_seriais = Bipagem.objects.count()
        nome_pa = "TODAS AS PAs"
        endereco_pa = "Consolidado Geral"

    else:
        # Usuários normais
        grupo = user.groups.first()
        nome_pa = grupo.name if grupo else "PA Não vinculada"
        endereco_pa = getattr(grupo.informacoes, "endereco", "Não informado") if grupo else "Não informado"

        lotes = LoteBipagem.objects.filter(user_created=user)
        total_lotes = lotes.count()
        total_caixas = Bipagem.objects.filter(id_caixa__lote__user_created=user).values('id_caixa').distinct().count()
        total_seriais = Bipagem.objects.filter(id_caixa__lote__user_created=user).count()

    context = {
        "empresa": "Getnet",
        "cnpj": "12.345.678/0001-99",
        "responsavel": responsavel,
        "nome_pa": nome_pa,
        "endereco_pa": endereco_pa,
        "data_emissao": datetime.now().strftime('%d/%m/%Y'),
        "resumo_pa": [{
            "lote": total_lotes,
            "caixas": total_caixas,
            "seriais": total_seriais,
        }],
        "total_caixas": total_caixas,
        "total_seriais": total_seriais,
    }

    template = get_template('inventario/extracao.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="laudo_pa.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response


@login_required(login_url='inventario:login')
def relatorios_view(request):
    user = request.user
    username = user.username.lower()

    usuarios_admins = ['adm_tecnico', 'adm_gtn', 'adm_auditoria']
    is_admin = username in usuarios_admins

    if is_admin:
        grupos = Group.objects.exclude(name__in=["INV_PA_GER_TOTAL", "INV_PA_VISUALIZADOR_MASTER"])
    else:
        grupos = user.groups.exclude(name__in=["INV_PA_GER_TOTAL", "INV_PA_VISUALIZADOR_MASTER"])

    pa_selecionada = request.GET.get('pa')
    dados_pa = []

    if pa_selecionada:
        lotes = LoteBipagem.objects.filter(group_user__name=pa_selecionada)
        for lote in lotes:
            total_seriais = Bipagem.objects.filter(id_caixa__lote=lote).count()
            total_caixas = lote.caixas.count()
            dados_pa.append({
                'lote': lote.numero_lote,
                'status': lote.status,
                'criado_por': lote.user_created.username,
                'total_caixas': total_caixas,
                'total_seriais': total_seriais
            })

    return render(request, 'inventario/relatorios.html', {
        'grupos': grupos,
        'dados_pa': dados_pa,
        'pa_selecionada': pa_selecionada,
    })