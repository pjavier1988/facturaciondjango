from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import generic
from django.db.models import F
from django.urls import reverse_lazy
from django.db.models.aggregates import Sum, Count
from rest_framework.test import APIRequestFactory
from datetime import datetime
from .models import Empresa, User, Links
from .forms import EmpresaForm, LinksForm
from fac.models import FacturaEnc, Cliente, FacturaDet
from api.views import ProductosAgotados
from inv.models import Producto
from cmp.models import Proveedor

#Empresa *************************************************************************************************************************************

def administracion(request):

    template_name = 'param/empresa_det.html'

    empresa = Empresa.objects.get(pk=request.user.company.id)
    links = Links.objects.filter(empresa=empresa)

    context = {
        'obj': empresa,
        'links': links,
    }

    return render(request, template_name, context)

class EmpresaView(LoginRequiredMixin, generic.ListView):

    model = Empresa
    template_name = "param/empresa_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

class EmpresaNew(LoginRequiredMixin, generic.CreateView):

    model = Empresa
    template_name = "param/empresa_form.html"
    context_object_name = "obj"
    form_class = EmpresaForm
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if set_user_company(self.request.user.id, self.object) == False:
            messages.error(self.request,'Super Usuario solo puede tener una empresa')
        return reverse_lazy('param:administracion_empresa')

class EmpresaEdit(LoginRequiredMixin, generic.UpdateView):

    model = Empresa
    template_name = "param/empresa_form.html"
    context_object_name = "obj"
    form_class = EmpresaForm
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('param:administracion_empresa')

# LINKS ****************************************************************************************************************************

class LinksNew(LoginRequiredMixin, generic.CreateView):

    model = Links
    template_name = "param/links_form.html"
    context_object_name = "obj"
    form_class = LinksForm
    login_url = "bases:login"
    success_url = reverse_lazy("param:administracion_empresa")
    success_message = "Link creado exitosamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)

#Reportes *************************************************************************************************************************************
#https://datatables.net/extensions/buttons/examples/initialisation/export.html

def compras_list(request):

    template_name = 'reportes/compras_list.html'

    compras = FacturaEnc.objects.filter(
        tipo="compra",
        empresa=request.user.company
    )
    total = 0

    if compras:
        for c in compras:
            total = total + c.total

    context = {
        'obj': compras,
        'total':total,
    }

    return render(request, template_name, context)

def ventas_list(request):

    template_name = 'reportes/ventas_list.html'

    compras = FacturaEnc.objects.filter(
        tipo="factura",
        empresa=request.user.company
    )

    total = 0

    if compras:
        for c in compras:
            total = total + c.total

    context = {
        'obj': compras,
        'total': total,
    }

    return render(request, template_name, context)

def venta_detail(request, factura_id):

    template_name = 'reportes/venta_detail.html'

    venta_enc = FacturaEnc.objects.get(pk=factura_id)
    ventas_det = FacturaDet.objects.filter(
        factura=venta_enc,
        empresa=request.user.company,
    )

    context = {
        'obj': venta_enc,
        'ventas': ventas_det,
    }

    return render(request, template_name, context)
def compra_detail(request, factura_id):

    template_name = 'reportes/compras_detail.html'

    compra_enc = FacturaEnc.objects.get(pk=factura_id)
    compra_det = FacturaDet.objects.filter(
        factura=compra_enc,
        empresa=request.user.company,
    )

    context = {
        'obj': compra_enc,
        'compras': compra_det,
    }

    return render(request, template_name, context)
def alerta_cantidad(request):

    template_name = 'reportes/alerta_cantidad_list.html'

    productos = Producto.objects.filter(existencia__lt=F('min_stock'), empresa=request.user.company)

    context = {
        'obj': productos,
    }

    return render(request, template_name, context)

def proveedores_list(request):

    template_name = 'reportes/proveedores_list.html'

    proveedores = Proveedor.objects.filter(empresa=request.user.company)

    context = {
        'obj': proveedores,
    }

    return render(request, template_name, context)

def clientes_list(request):

    template_name = 'reportes/clientes_list.html'

    clientes = Cliente.objects.filter(empresa=request.user.company)

    context = {
        'obj': clientes,
    }

    return render(request, template_name, context)

def proveedor_history(request, proveedor_id):

    template_name = 'reportes/proveedor_history.html'

    proveedor = Proveedor.objects.get(pk=proveedor_id, empresa=request.user.company)
    compras = FacturaEnc.objects.filter(
        tipo="compra",
        proveedor=proveedor,
        empresa=request.user.company,
    )

    nro_productos = FacturaDet.objects.filter(
        factura__tipo="compra",
        factura__proveedor=proveedor,
        empresa=request.user.company,
    ).aggregate(Sum('cantidad'))

    gasto_total = FacturaDet.objects.filter(
        factura__tipo="compra",
        factura__proveedor=proveedor,
        empresa=request.user.company,
    ).aggregate(Sum('factura__total'))

    nro_compras = FacturaDet.objects.filter(
        factura__tipo="compra",
        factura__proveedor=proveedor,
        empresa=request.user.company,
    ).count()

    context = {
        'proveedor': proveedor,
        'compras': compras,
        'reportes': {
            'nro_productos': get_sum(nro_productos, "cantidad"),
            'gasto_total': get_sum(gasto_total, "factura__total"),
            'nro_compras': nro_compras,
        }
    }

    return render(request, template_name, context)

def cliente_history(request, cliente_id):

    template_name = 'reportes/cliente_history.html'

    cliente = Cliente.objects.get(pk=cliente_id, empresa=request.user.company)

    compras = FacturaEnc.objects.filter(
        tipo="factura",
        cliente=cliente,
        empresa=request.user.company,
    )

    nro_productos = FacturaDet.objects.filter(
        factura__tipo="factura",
        factura__cliente=cliente,
        empresa=request.user.company,
    ).aggregate(Sum('cantidad'))

    gasto_total = FacturaDet.objects.filter(
        factura__tipo="factura",
        factura__cliente=cliente,
        empresa=request.user.company,
    ).aggregate(Sum('factura__total'))

    nro_compras = FacturaDet.objects.filter(
        factura__tipo="factura",
        factura__cliente=cliente,
        empresa=request.user.company,
    ).count()

    context = {
        'cliente': cliente,
        'ventas': compras,
        'reportes': {
            'nro_productos': get_sum(nro_productos, "cantidad"),
            'gasto_total': get_sum(gasto_total, "factura__total"),
            'nro_compras': nro_compras,
        }
    }

    return render(request, template_name, context)

def devolucion_compras_list(request):

    template_name = 'reportes/devolucion_compras_list.html'

    compras = FacturaEnc.objects.filter(
        tipo="compra",
        estado_pago='No Pagado',
        empresa=request.user.company
    )

    context = {
        'compras': compras
    }

    return render(request, template_name, context)

def devolucion_facturas_list(request):

    template_name = 'reportes/devolucion_facturas_list.html'

    facturas = FacturaEnc.objects.filter(
        tipo="factura",
        estado_pago='No Pagado',
        empresa=request.user.company
    )

    context = {
        'facturas': facturas
    }

    return render(request, template_name, context)

def almacen_list(request):

    template_name = 'reportes/almacen_list.html'

    current_year = datetime.now().year
    current_month = datetime.now().month
    fechagte=datetime(current_year, current_month, 1)
    next_month = current_month + 1

    if(next_month==13):
        next_month=1

    fechalte=datetime(current_year, next_month, 1)

    facturas_year = FacturaEnc.objects.filter(fecha__year=current_year,tipo="factura", empresa=request.user.company).aggregate(Sum('total'))
    facturas_mes = FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="factura", empresa=request.user.company).aggregate(Sum('total'))

    compras_year = FacturaEnc.objects.filter(fecha__year=current_year,tipo="compra", empresa=request.user.company).aggregate(Sum('total'))
    compras_mes = FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="compra", empresa=request.user.company).aggregate(Sum('total'))

    #Productos
    productos = Producto.objects.filter(empresa=request.user.company, estado=1, existencia__gt=0)
    valor_productos = 0
    cantidad_productos = 0

    for p in productos:

        valor_productos = valor_productos + (p.precio * p.existencia)
        cantidad_productos = cantidad_productos + 1

    compras = FacturaEnc.objects.filter(tipo="compra", empresa=request.user.company)
    ventas = FacturaEnc.objects.filter(tipo="factura", empresa=request.user.company)

    clientes = Cliente.objects.filter(empresa=request.user.company)
    proveedores = Proveedor.objects.filter(empresa=request.user.company)

    facturas_year = get_total(facturas_year)
    compras_year = get_total(compras_year)
    facturas_mes = get_total(facturas_mes)
    compras_mes = get_total(compras_mes)

    ganancias_anual = facturas_year - compras_year
    ganancias_mensual = facturas_mes - compras_mes

    context = {
        'productos': productos,
        'valor_productos': valor_productos,
        'cantidad_productos': cantidad_productos,
        'ventas_mes':f"${facturas_mes}",
        'ventas_anual':f"${facturas_year}",
        'ganancias_mensual':f"${ganancias_mensual}",
        'ganancias_anual':f"${ganancias_anual}",
        'compra':compras,
        'venta':ventas,
        'cliente':clientes,
        'proveedor':proveedores,
    }

    return render(request, template_name, context)

def kardex(request, producto_id):

    template_name = 'reportes/kardex.html'
    producto = Producto.objects.get(pk=producto_id)

    facturas = FacturaDet.objects.filter(
        producto=producto,
        empresa=request.user.company,
        estado=1,
    ).order_by('fm')

    _catidad = 0
    _total = 0
    _facturas = {}

    for f in facturas:

        if f.factura.tipo == 'compra':
            _catidad = _catidad + f.cantidad
            _total = _total + f.total
        else:
            _catidad = _catidad - f.cantidad
            _total = _total - f.total

        _facturas[str(f.id) + '_c'] = _catidad
        _facturas[str(f.id) + '_t'] = _total

        print(_facturas)

    context = {
        'producto': producto,
        'facturas': facturas,
        'factura_data': _facturas,
    }

    return render(request, template_name, context)

def nomina2(request):

    template_name = 'param/nomina2.html'

    context = {
    }

    return render(request, template_name, context)

#Funciones

def get_total(data):

    if data.get('total__sum'):

        return data.get('total__sum')
    else:
        return 0

def set_user_company(user_id, company):

    user = User.objects.filter(pk=user_id).first()

    if user:
        if user.company == None:
            user.company = company
            user.save()
            return True
        else:
            return False

# Custom Filters
#https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
from django.template.defaulttags import register

@register.filter
def get_factura_cantidad(dictionary, id):
    return dictionary.get(f'{id}_c')

@register.filter
def get_factura_total(dictionary, id):
    return dictionary.get(f'{id}_t')

@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)

# Methods

def get_sum(data, field):

    if data.get(f'{field}__sum'):

        return data.get(f'{field}__sum')
    else:
        return 0
