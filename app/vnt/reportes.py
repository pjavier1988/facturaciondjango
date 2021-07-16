from django.shortcuts import render
from .models import *
from fac.models import  Cliente
from inv.models import Producto

def imprimir_cotizacion(request, id):
    template_name = "vnt/cotizacion_print.html"

    cot = Cotizacion.objects.get(id=id)
    productos = ProductosCotizacion.objects.filter(cotizacion_id = cot.id)

    context={
        'request':request,
        'cot':cot,
        'productos':productos,
    }

    return render(request, template_name, context)

def detalle_cotizacion(request, id):
    template_name = "vnt/detalle_cotizacion.html"

    cot = Cotizacion.objects.get(id=id)
    productos = ProductosCotizacion.objects.filter(cotizacion_id = cot.id)

    context={
        'request':request,
        'cot':cot,
        'productos':productos,
    }
    return render(request, template_name, context)
