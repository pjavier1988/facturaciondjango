from django import forms
from django.forms import fields, widgets
from .models import Empresa, Links

class EmpresaForm(forms.ModelForm):
    
    class Meta:
        model = Empresa
        fields = ['logo','nombre','nombre_completo', 'telefono', 'direccion', 'correo', 'ruc', 'tributa', 'pais']
        labels = {
            "nombre" : "Nombre",
            "nombre_completo" : "Nombre Completo",
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'correo': 'Correo',
            'ruc': 'RUC',
            'tributa': 'Tributa',
            'pais': 'País',
        }
        widgets={
            "nombre_completo":forms.TextInput,
            "correo": forms.EmailInput,
        }

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'mx-5 mt-1 form-control' 
            })

        self.fields['telefono'].widget.attrs['pattern'] = '^[0-9]{10,15}'
        self.fields['logo'].widget.attrs['accept'] = 'image/*'

class LinksForm(forms.ModelForm):

    class Meta:
        model = Links
        fields = ['plataforma', 'url', 'imagen', 'estado']
        labels = {
            'plataforma': 'Plataforma',
            'url': 'URL',
            'imagen': 'Imágen',
            'estado': 'Estado',
        }

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'mx-5 mt-1 form-control',
            })