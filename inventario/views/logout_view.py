from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='inventario:login')
def logout_view(request):
    logout(request)
    return redirect('inventario:login')