from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def download_extracao_pdf(request):
    template_path = 'inventario/extracao.html'
    context = {}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="extracao.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response