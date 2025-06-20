from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required(login_url='inventario:login')
def acompanhamento_dash(request):
    is_visualizador_master = request.user.groups.filter(name='INV_PA_VISUALIZADOR_MASTER').exists()

    if not is_visualizador_master:
         return redirect('inventario:index')

    return render(request, 'inventario/acompanhamento.html', {
        'is_visualizador_master': is_visualizador_master,
    })