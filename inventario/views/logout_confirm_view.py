from django.contrib.auth import logout
from django.shortcuts import render, redirect

def logout_confirm_view(request):
    return render(request, 'inventario/logout_confirm.html')
