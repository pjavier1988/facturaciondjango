from django import forms
from django.forms import fields, widgets
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    
    class Meta:
        model = Empresa
        fields = ['logo', 'nombre','nombre_completo', 'telefono', 'direccion', 'correo', 'ruc']
        exclude =["um","fm","uc","fc"]
        labels = {
            "nombre" : "Nombre",
            "nombre_completo" : "Nombre Completo",
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'correo': 'Correo',
            'logo': 'Logo URL',
            'ruc': 'RUC'
        }
        widgets={"nombre_completo":forms.TextInput}

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'mx-5 mt-1 form-control' 
            })