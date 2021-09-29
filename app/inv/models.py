from django.db import models
from bases.models import ClaseModelo
from param.models import Empresa

class Categoria(ClaseModelo):

    descripcion = models.CharField(max_length =100, help_text = 'Descripción', unique = True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria,self).save()

    class Meta:
        verbose_name_plural = "Categorías"

class SubCategoria(ClaseModelo):

    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length =100, help_text = 'Descripción')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}:{}'.format(self.categoria.descripcion,self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria,self).save()

    class Meta:
        verbose_name_plural = "Sub Categorías"
        unique_together = ("categoria","descripcion")

class Marca(ClaseModelo):

    descripcion = models.CharField(max_length =100, help_text = 'Descripción', unique = True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Marca,self).save()

    class Meta:
        verbose_name_plural = "Marcas"

class UnidadMedida(ClaseModelo):

    descripcion = models.CharField(max_length =100, help_text = 'Descripción', unique = True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(UnidadMedida,self).save()

    class Meta:
        verbose_name_plural = "Unidades de medida"

class Producto(ClaseModelo):

    codigo = models.CharField(max_length =20, unique = True)
    codigo_barras = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.FloatField(default=0)
    existencia = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=0)
    ultima_compra = models.DateField(null=True, blank=True)
    tiene_iva = models.BooleanField(default=False)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, blank=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    es_servicio = models.BooleanField(default=False)
    imagen = models.FileField(upload_to='img/productos', null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()

    @property
    def imagen_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url

    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ("codigo","codigo_barras")

class Perdidas(ClaseModelo):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False, blank=False)
    cantidad = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=1000)
    fecha=models.DateTimeField(auto_now_add=True)
