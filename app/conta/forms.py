from django.forms import fields, widgets
from django.conf import settings
from django import forms
from .models import Empleado, Rol, EmpleadoHoraExtra, HoraExtra

class RolForm(forms.ModelForm):

    class Meta:

        model = Rol
        fields = ['rol','salario','dias_laborales']
        labels = {
            "rol" : "Nombre del Rol/Cargo",
            "salario" : "Salario",
            'dias_laborales': 'Nro. Días laborales',
        }

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class EmpleadoForm(forms.ModelForm):

    class Meta:

        model = Empleado
        fields = ['identificacion','nombres','apellidos','direccion','celular','correo','rol']
        labels = {
            "identificacion" : "CI/Pasaporte",
            "nombres" : "Nombres",
            "apellidos" : "Apellidos",
            "direccion" : "Dirección",
            "celular" : "Celular/Teléfono",
            "correo" : "Correo",
            "rol" : "Rol/Cargo",
        }

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'd-flex form-control mx-1 my-1 text-center width-max'
            })

        self.fields['rol'].queryset = Rol.objects.filter(estado=True, empresa=user.company).order_by("salario")
        self.fields['rol'].empty_label = "Seleccione un Rol/Cargo"

class HoraExtraForm(forms.ModelForm):

    class Meta:

        model = HoraExtra
        fields = ['nombre','siglas','recargo','factor']
        labels = {
            "nombre" : "Nombre",
            "siglas" : "Siglas",
            'recargo': 'Recargo (%)',
            'factor': 'Factor Multiplicador',
        }

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'd-flex form-control mx-1 my-1 text-center width-max'
            })

class EmpleadoHoraExtraForm(forms.ModelForm):

    class Meta:

        model = EmpleadoHoraExtra
        fields = ['empleado','hora_extra','horas','desc','fecha']
        labels = {
            "empleado" : "Empleado",
            "hora_extra" : "Concepto",
            "horas" : "Horas",
            "desc" : "Observación",
            "fecha" : "Fecha",
        }
        widgets={
            "desc": forms.Textarea(attrs={
                'rows': 3,
            }),
            'fecha': forms.TextInput(attrs={
                'type': 'datetime-local',
            }),
        }

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'd-flex form-control mx-1 my-1 text-center width-max'
            })

        self.fields['empleado'].queryset = Empleado.objects.filter(estado=True, empresa=user.company).order_by("apellidos")
        self.fields['empleado'].empty_label = "Seleccione un empleado"
        self.fields['hora_extra'].queryset = HoraExtra.objects.filter(estado=True, empresa=user.company).order_by("nombre")
        self.fields['hora_extra'].empty_label = "Seleccione un concepto"