from django.db import models
from bases.models import ClaseModelo
from param.models import Empresa

class Rol(ClaseModelo):

    rol = models.CharField(max_length=100, help_text='Rol')
    salario = models.FloatField(default=0)
    dias_laborales = models.IntegerField(default=30)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}'.format(self.rol)

    class Meta:
        verbose_name_plural = "Roles"

class Empleado(ClaseModelo):
    
    identificacion = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300)
    celular = models.CharField(max_length=20, null=True, blank=True)
    correo = models.CharField(max_length=60)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=False, blank=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Empleado, self).save()

    def __str__(self):
        return '{} {}'.format(self.apellidos,self.nombres)

    class Meta:
        verbose_name_plural = "Empleados"