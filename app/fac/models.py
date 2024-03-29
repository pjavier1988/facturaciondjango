from cmp.models import Proveedor
from django.db import models
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Max
from bases.models import ClaseModelo, ClaseModelo2
from inv.models import Producto
from param.models import Empresa

class Cliente(ClaseModelo):

    NAT='Natural'
    JUR='Jurídica'

    TIPO_CLIENTE = [(NAT,'Natural'),(JUR,'Jurídica')]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=13)
    celular = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField( max_length=10, choices=TIPO_CLIENTE, default=NAT)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.apellidos,self.nombres)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = "Clientes"

    
class FacturaEnc(ClaseModelo2):

    PAG = 'Pagado'
    PAR = 'Parcial'
    NOPAG = 'No Pagado' #Devuelto

    ESTADOS_PAGO = [(PAG,'Pagado'),(PAR,'Parcial'), (NOPAG, 'No Pagado')]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(auto_now_add=True,editable=True)
    sub_total = models.FloatField(default=0)
    faciva = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE, null=True)
    observacion = models.TextField(blank=True,null=True)
    no_factura = models.IntegerField(null=True)
    fecha_factura = models.DateField()
    fecha_compra = models.DateField()
    tipo = models.CharField(max_length=100)
    estado_pago = models.TextField(null=False, choices=ESTADOS_PAGO, default=PAG)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        
        if self.observacion:
            self.observacion = self.observacion.upper()

        if self.sub_total == None  or self.descuento == None:
            self.sub_total = 0
            self.descuento = 0

        no_factura_max = FacturaEnc.objects.count()
        self.no_factura = int(no_factura_max) + 1
        self.total = self.sub_total - self.descuento
        self.total = self.sub_total - self.descuento + self.faciva

        super(FacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name="Encabezado Factura"
        permissions = [
            ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
        ]
    

class FacturaDet(ClaseModelo2):

    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    detiva = models.FloatField(default=0)
    precio_prv = models.FloatField(default=0)
    costo = models.FloatField(default=0)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        if self.factura.tipo == 'factura':
            total = float(float(int(self.cantidad)) * float(self.precio))
            iva = total - round(total/1.19,2) 
            self.sub_total = total -iva
            
            self.detiva = iva
            self.total = self.sub_total - float(self.descuento) + self.detiva

        if self.factura.tipo == 'compra':
            self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
            self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name="Detalle Factura"
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]


@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender,instance,**kwargs):
    
    factura_id = instance.factura.id
    producto_id = instance.producto.id

    enc = FacturaEnc.objects.get(pk=factura_id)
    
    if enc:
        sub_total = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(sub_total=Sum('sub_total')) \
            .get('sub_total',0.00)

        detiva = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(detiva=Sum('detiva')) \
            .get('detiva',0.00)
        
        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
        
        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.faciva = detiva
        enc.save()

    prod=Producto.objects.filter(pk=producto_id).first()

    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()