from django.shortcuts import render, redirect
from ..models import LoteBipagem
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def criar_lote_view(request):
    if request.method == 'POST':
        grupo = request.user.groups.first()
        if grupo:
            nome_grupo = grupo.name
            if nome_grupo.startswith("INV_PA_"):
                nome_exibicao = nome_grupo.replace("INV_PA_", "", 1)
            else:
                nome_exibicao = nome_grupo

            lote= LoteBipagem.objects.create(
                user_created=request.user,
                group_user=grupo,
                group_user_txt=nome_exibicao
            )

        return redirect('inventario:lote', lote.id) 
    return render(request, 'inventario/criar_lote.html')