from django.shortcuts import render, get_object_or_404, redirect
from ..models import Caixa
from ..forms import CaixaForm  # Supondo que esse form já existe

def editar_caixa(request, lote_id, caixa_id):
    caixa = get_object_or_404(Caixa, id=caixa_id, lote__id=lote_id)

    if request.method == 'POST':
        form = CaixaForm(request.POST, instance=caixa)
        if form.is_valid():
            form.save()
            return redirect('inventario:lote', lote_id=caixa.lote.id)
    else:
        form = CaixaForm(instance=caixa)

    return render(request, 'inventario/editar_caixa.html', {
        'form': form,
        'caixa': caixa,
    })
