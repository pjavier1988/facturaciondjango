from django import forms
from django.forms import fields, widgets
from .models import Cotizacion
from django.conf import settings

class CotizacionForm(forms.ModelForm):

    class Meta:

        model = Cotizacion
        fields = '__all__'
        labels = {}
        widgets={}

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })
