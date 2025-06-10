from django.shortcuts import render, get_object_or_404, redirect
from ..models import LoteBipagem
from ..forms import CaixaForm

def lote(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)

    if request.method == 'POST':
        form = CaixaForm(request.POST)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.lote = lote
            caixa.save()
            return redirect('home')
    else:
        form = CaixaForm()

    return render(request, 'inventario/criar_caixa.html', {'form': form, 'lote': lote})
