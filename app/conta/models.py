from django.db import models
from bases.models import ClaseModelo
from param.models import Empresa

class Rol(ClaseModelo):

    rol = models.CharField(max_length=100, help_text='Rol')
    salario = models.FloatField(default=0)
    dias_laborales = models.IntegerField(default=30)

    def __str__(self) :
        return '{}'.format(self.rol)

    class Meta:
        verbose_name_plural = "Roles"

class Empleado(ClaseModelo):
    
    identificacion = models.CharField(max_length=20, help_text='Identificación', unique=True)
    nombres = models.CharField(max_length=100, help_text='Nombres')
    apellidos = models.CharField(max_length=100, help_text='Apellidos')
    direccion = models.CharField(max_length=300, help_text='Dirección')
    celular = models.CharField(max_length=20, help_text='celular', null=True, blank=True)
    correo = models.CharField(max_length=60, help_text='Correo')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=False, blank=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) :
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name_plural = "Empleados"