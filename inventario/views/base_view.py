from django.shortcuts import render
from ..models import LoteBipagem
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def index(request):
    lotes = LoteBipagem.objects.all().order_by('-criado_em')
    return render(request, 'inventario/index.html', {'lotes': lotes})