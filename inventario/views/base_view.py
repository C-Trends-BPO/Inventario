from django.shortcuts import render, redirect, get_object_or_404
from ..models import LoteBipagem
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def index(request):
    if request.method == 'POST' and 'fechar_lote_id' in request.POST:
        lote_id = request.POST.get('fechar_lote_id')
        lote = get_object_or_404(LoteBipagem, id=lote_id)
        lote.status = 'processando'  # ou 'processando', se preferir
        lote.save()
        return redirect('inventario:index')

    lotes = LoteBipagem.objects.all().order_by('-criado_em')
    return render(request, 'inventario/index.html', {'lotes': lotes})