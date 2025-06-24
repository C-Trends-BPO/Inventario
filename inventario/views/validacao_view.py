from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..models import Caixa, LoteBipagem, Bipagem
import math
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

@login_required(login_url='inventario:login')
def validar_lote_view(request, lote_id):
    lote = get_object_or_404(LoteBipagem, id=lote_id)

    # Bloqueia validação para usuários visualizadores
    if request.method == 'POST' and request.user.groups.filter(name='Visualizador Master').exists():
        return HttpResponseForbidden("Você não tem permissão para validar lotes.")
    
    seriais = lote.bipagem.all()
    total_seriais = seriais.count()
    amostra_necessaria = math.ceil(total_seriais * 0.05)

    context = {
        "lote": lote,
        "total_seriais": total_seriais,
        "amostra_necessaria": amostra_necessaria,
    }

    return render(request, "inventario/validar_lote.html", context)

@login_required(login_url='inventario:login')
@csrf_exempt
def validar_serial(request, lote_id):
    if request.method == "POST":
        if request.user.groups.filter(name='INV_PA_VISUALIZADOR_MASTER').exists():
            return JsonResponse({
                "status": "erro",
                "mensagem": "❌ Você não tem permissão para validar seriais."
            })

        lote = get_object_or_404(LoteBipagem, id=lote_id)
        codigo = request.POST.get("codigo", "").strip().upper()

        serial_valido = lote.bipagem.filter(nrserie=codigo).exists()

        if not serial_valido:
            lote.status = "cancelado"
            lote.save()
            return JsonResponse({"status": "erro", "mensagem": f"❌ Serial {codigo} inválido. Lote cancelado."})

        # Aqui você pode mudar o status do lote também, se quiser
        lote.status = "fechado"
        lote.save()

        return JsonResponse({
            "status": "ok",
            "mensagem": "✅ Serial validado com sucesso!",
            "redirect_url": reverse('inventario:index')
        })

    return JsonResponse({"status": "erro", "mensagem": "Método não permitido"}, status=405)

@login_required(login_url='inventario:login')
@require_POST
@csrf_exempt
def finalizar_lote_view(request, lote_id):
    if request.user.groups.filter(name='INV_PA_VISUALIZADOR_MASTER').exists():
        return JsonResponse({
            "status": "erro",
            "mensagem": "❌ Você não tem permissão para finalizar lotes."
        })

    lote = get_object_or_404(LoteBipagem, id=lote_id)

    if lote.caixas.filter(status='Iniciada').exists():
        return JsonResponse({
            "status": "erro",
            "mensagem": "❌ O lote possui bipagens abertas. Finalize todas as bipagens antes de concluir o lote."
        })

    caixas = Caixa.objects.filter(lote_id=lote_id)

    if not caixas.exists():
        return JsonResponse({
            "status": "erro",
            "mensagem": "❌ Para finalizar o lote, é necessário iniciar uma bipagem antes."
        })

    lote.status = 'fechado'
    lote.save()

    return JsonResponse({
        "status": "ok",
        "mensagem": "✅ Lote finalizado com sucesso!",
        "redirect_url": reverse('inventario:index')
    })