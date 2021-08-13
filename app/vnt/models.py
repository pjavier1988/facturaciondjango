from django.db import models
from fac.models import Cliente
from bases.models import ClaseModelo
from inv.models import Producto
from param.models import Empresa
import datetime

class Cotizacion(ClaseModelo):

    ENV = 'Enviado'
    PEN = 'Pendiente'

    ESTADOS_COTIZACION = [(ENV,'Enviado'),(PEN,'Pendiente'),]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    estado_cotizacion = models.TextField(null=False, choices=ESTADOS_COTIZACION, default=ENV)
    iva = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    envio = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    total = models.FloatField(default=0)
    nota = models.TextField(null=True, max_length=300)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

class ProductosCotizacion(ClaseModelo):

    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, null=False, blank=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False, blank=False)
    cantidad = models.IntegerField(default=1)
    descuento = models.FloatField(default=0)
