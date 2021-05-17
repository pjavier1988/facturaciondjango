from django import forms
from django.forms import fields, widgets
from .models import Categoria, Producto,SubCategoria,Marca, UnidadMedida

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
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by("descripcion")
    )
    class Meta:
        model = SubCategoria
        fields = ['categoria','descripcion','estado']
        labels = {
            "descripcion" : "SubCategoría'",
            "estado" : "Estado"
        }
        widgets={"descripcion":forms.TextInput}

    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })
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

    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo','codigo_barras','descripcion',\
            'estado','precio','existencia','ultima_compra',\
                'marca','subcategoria','unidad_medida','tiene_iva']
        labels = {
            "descripcion" : "Descripción del Producto'",
            "estado" : "Estado"
        }
        exclude =["um","fm","uc","fc"]
        widgets={"descripcion":forms.TextInput}

    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True
