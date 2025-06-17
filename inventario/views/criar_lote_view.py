from django.shortcuts import render, redirect
from ..models import LoteBipagem
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def criar_lote_view(request):
    if request.method == 'POST':
        lote= LoteBipagem.objects.create(
            user_created=request.user,
            group_user=request.user.groups.first(),
        )
        lote_id  = lote.id
        return redirect('inventario:lote', lote_id) 
    return render(request, 'inventario/criar_lote.html')