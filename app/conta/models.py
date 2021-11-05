from django.db import models
from bases.models import ClaseModelo
from param.models import Empresa

HORAS_BASE = 8
SALARIO_BASICO = 908.526
DIAS_LABORALES = 30

class Rol(ClaseModelo):

    rol = models.CharField(max_length=100, help_text='Rol')
    salario = models.FloatField(default=0)
    dias_laborales = models.IntegerField(default=DIAS_LABORALES)
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

class HoraExtra(ClaseModelo):

    nombre = models.CharField(max_length=200, null=False, blank=False, unique=True)
    siglas = models.CharField(max_length=10, null=True, blank=True)
    recargo = models.FloatField(default=0)
    factor = models.FloatField(null=False, blank=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def save(self):
        self.nombre = self.nombre.upper()
        super(HoraExtra, self).save()

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name_plural = "HorasExtras"

#Modelo de relación entre la tabla de empleados y horas extras
class EmpleadoHoraExtra(ClaseModelo):

    horas = models.FloatField(default=0, null=True)
    valor_hora = models.FloatField(null=False, blank=False)
    total = models.FloatField(null=False, blank=False)
    desc = models.CharField(max_length=200, null=True, blank=True)
    fecha = models.DateTimeField(null=False, blank=False)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=False, blank=False)
    hora_extra = models.ForeignKey(HoraExtra, on_delete=models.CASCADE, null=False, blank=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.total)