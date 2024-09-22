from django.shortcuts import render

from logs.models import Logs_sistema
from utils.paginador import paginador_general


def crear_log_sistema(user, accion, detalle, modelo):
    Logs_sistema.objects.create(user=user ,
            accion=accion,
            detalle=detalle,
            modelo=modelo
            )
    return

def log_materiales(request):
    logs = Logs_sistema.objects.filter(modelo='Materiales')
    logs= paginador_general(request, logs)
    context={
        'data':logs
    }
    return render(request, 'logs/logs.sistema.html', context)

def log_categorias(request):
    logs = Logs_sistema.objects.filter(modelo='Categoria')
    logs= paginador_general(request, logs)
    context={
        'data':logs
    }
    return render(request, 'logs/logs.sistema.html', context)

def log_usuarios(request):
    logs = Logs_sistema.objects.filter(modelo='Usuario')
    logs= paginador_general(request, logs)
    context={
        'data':logs
    }
    return render(request, 'logs/logs.sistema.html', context)

