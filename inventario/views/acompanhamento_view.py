from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def acompanhamento_dash(request):
    is_visualizador_master = request.user.groups.filter(
        name__in=['INV_PA_VISUALIZADOR_MASTER', 'INV_PA_GER_TOTAL']
    ).exists()

    if not is_visualizador_master:
        return redirect('inventario:index')

    return render(request, 'inventario/acompanhamento.html', {
        'is_visualizador_master': is_visualizador_master,
    })