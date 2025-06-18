from django.shortcuts import render

def acompanhamento_dash(request):
    is_visualizador_master = request.user.groups.filter(name='INV_VISUALIZADOR_MASTER').exists()
    return render(request, 'inventario/acompanhamento.html', {
        'is_visualizador_master': is_visualizador_master, 
    })