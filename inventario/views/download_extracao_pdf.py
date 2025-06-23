from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Count
from inventario.models import LoteBipagem
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def download_extracao_pdf(request):
    user = request.user
    grupo = user.groups.first()
    endereco_pa = getattr(grupo.informacoes, "endereco", "Não informado")
    responsavel = request.user.get_full_name() or request.user.username

    if not grupo:
        return HttpResponse('Usuário sem grupo vinculado.', status=403)

    lotes = (
        LoteBipagem.objects
        .filter(group_user=grupo)
        .annotate(
            qtd_caixas=Count('caixas', distinct=True),
            qtd_seriais=Count('caixas__bipagem', distinct=True),
        )
        .order_by('numero_lote')
    )

    resumo_pa = []
    total_caixas = 0
    total_seriais = 0

    for lote in lotes:
        resumo_pa.append({
            "lote": lote.numero_lote,
            "caixas": lote.qtd_caixas,
            "seriais": lote.qtd_seriais,
        })
        total_caixas += lote.qtd_caixas
        total_seriais += lote.qtd_seriais

    context = {
        "empresa": "C-Trends BPO",
        "endereco": "R. Bonfim, 81 - Maranhão, São Paulo - SP, 03073-010",
        "cnpj": "12.345.678/0001-99",
        "responsavel": responsavel,
        "nome_pa": grupo.name,
        "endereco_pa": endereco_pa,
        "data_emissao": datetime.now().strftime('%d/%m/%Y'),
        "resumo_pa": resumo_pa,
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