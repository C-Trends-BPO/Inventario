from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Count
from inventario.models import LoteBipagem, Bipagem
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import Group

@login_required(login_url='inventario:login')
def download_extracao_pdf(request):
    user = request.user
    responsavel = user.get_full_name() or user.username
    grupos = user.groups.values_list('name', flat=True)

    is_admin_total = 'INV_PA_GER_TOTAL' in grupos 

    if is_admin_total:
        lotes = LoteBipagem.objects.all()
        total_lotes = lotes.count()
        total_caixas = Bipagem.objects.values('id_caixa').distinct().count()
        total_seriais = Bipagem.objects.count()
        nome_pa = "TODAS AS PAs"
        endereco_pa = "Consolidado Geral"
    else:
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
    grupos = Group.objects.filter(name__startswith='INV_PA_')
    return render(request, 'inventario/relatorios.html', {'grupos': grupos})