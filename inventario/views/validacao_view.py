from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..models import LoteBipagem, Bipagem
import math

def validar_lote_view(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    
    seriais = lote.bipagem.all()
    total_seriais = seriais.count()
    amostra_necessaria = math.ceil(total_seriais * 0.05)

    context = {
        "lote": lote,
        "total_seriais": total_seriais,
        "amostra_necessaria": amostra_necessaria,
    }

    return render(request, "inventario/validar_lote.html", context)


@csrf_exempt
def validar_serial(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(LoteBipagem, id=lote_id)
        codigo = request.POST.get("codigo", "").strip().upper()

        serial_valido = lote.bipagem.filter(nrserie=codigo).exists()

        if not serial_valido:
            lote.status = "cancelado"
            lote.save()
            return JsonResponse({"status": "erro", "mensagem": f"❌ Serial {codigo} inválido. Lote cancelado."})

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "erro", "mensagem": "Método não permitido"}, status=405)

@require_POST
@csrf_exempt
def finalizar_lote_view(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)
    lote.status = 'fechado' 
    lote.save()
    return JsonResponse({"status": "ok", "mensagem": "Lote fechado com sucesso!"})