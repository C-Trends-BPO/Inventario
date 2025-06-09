from django.shortcuts import render, redirect
from ..models import LoteBipagem

def criar_lote_view(request):
    if request.method == 'POST':
        LoteBipagem.objects.create()
        return redirect('inventario:index') 
    return render(request, 'inventario/criar_lote.html')