from django import forms
from django.forms import fields, widgets
from .models import Categoria, Producto,SubCategoria,Marca, UnidadMedida
from django.conf import settings

class CategoriaForm(forms.ModelForm):

    class Meta:

        model = Categoria
        fields = ['descripcion','estado']
        labels = {
            "descripcion" : "Descripción de la Categoría'",
            "estado" : "Estado"
        }
        widgets={"descripcion":forms.TextInput}

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class SubCategoriaForm(forms.ModelForm):
    
    categoria = forms.ModelChoiceField(queryset=None)

    class Meta:

        model = SubCategoria
        fields = ['categoria','descripcion','estado']
        labels = {
            "categoria":"Categoria",
            "descripcion" : "Sub Categoría'",
            "estado" : "Estado"
        }
        widgets={"descripcion":forms.TextInput}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args,**kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

        #https://www.iteramos.com/pregunta/57707/django-modelchoicefield-filtrado-de-la-consulta-conjunto-y-configuracion-de-valor-predeterminado-como-un-objeto
        self.fields['categoria'].queryset = Categoria.objects.filter(estado=True, empresa=user.company).order_by("descripcion")
        self.fields['categoria'].empty_label = "Seleccione Categoría"

class MarcaForm(forms.ModelForm):

    class Meta:

        model = Marca
        fields = ['descripcion','estado']
        labels = {
            "descripcion" : "Descripción de la Marca'",
            "estado" : "Estado"
        }
        widgets={"descripcion":forms.TextInput}

    def __init__(self,*args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class UnidadMedidaForm(forms.ModelForm):

    class Meta:

        model = UnidadMedida
        fields = ['descripcion','estado']
        labels = {
            "descripcion" : "Descripción de la Unidad de Medida'",
            "estado" : "Estado"
        }
        widgets={"descripcion":forms.TextInput}

    def __init__(self, *args, **kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class ProductoForm(forms.ModelForm):

    class Meta:

        model = Producto
        fields = ['imagen','codigo','codigo_barras','descripcion','estado','precio','existencia', 'min_stock','ultima_compra','marca','subcategoria','unidad_medida','tiene_iva']
        labels = {
            "descripcion" : "Descripción del Producto",
            "estado" : "Estado",
            "min_stock":"Mínima Existencia",
            'tiene_iva': 'IVA',
        }
        exclude =["um","fm","uc","fc"]
        widgets={"descripcion":forms.TextInput}

    def __init__(self, user, *args,**kargs):

        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'd-flex form-control mx-1 my-1 text-center width-max',
            })

        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True
        self.fields['marca'].queryset = Marca.objects.filter(estado=True, empresa=user.company).order_by("descripcion")
        self.fields['subcategoria'].queryset = SubCategoria.objects.filter(estado=True, empresa=user.company).order_by("descripcion")
        self.fields['unidad_medida'].queryset = UnidadMedida.objects.filter(estado=True, empresa=user.company).order_by("descripcion")
        self.fields['imagen'].widget.attrs['accept'] = 'image/*'