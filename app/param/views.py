from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.test import APIRequestFactory
from django.contrib import messages
from django.views import generic
from django.db.models import F
from django.db.models.aggregates import Sum, Count
from .models import Empresa, User
from .forms import EmpresaForm
from fac.models import FacturaEnc, Cliente, FacturaDet
from api.views import ProductosAgotados
from inv.models import Producto
from cmp.models import Proveedor
from datetime import datetime

#Empresa *************************************************************************************************************************************

class EmpresaView(LoginRequiredMixin, generic.ListView):

    model = Empresa
    template_name = "param/empresa_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

class EmpresaDet(LoginRequiredMixin, generic.DetailView):

    model = Empresa
    template_name = "param/empresa_det.html"
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
        return reverse_lazy('param:empresa_det', kwargs={'pk': self.object.pk})

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
        return reverse_lazy('param:empresa_det', kwargs={'pk': self.object.pk})

#Reportes *************************************************************************************************************************************
#https://datatables.net/extensions/buttons/examples/initialisation/export.html

def compras_list(request):

    template_name = 'reportes/compras_list.html'

    compras = FacturaEnc.objects.filter(
        tipo="compra",
        empresa=request.user.company
    )

    context = {
        'obj': compras
    }

    return render(request, template_name, context)

def ventas_list(request):

    template_name = 'reportes/ventas_list.html'

    compras = FacturaEnc.objects.filter(
        tipo="factura",
        empresa=request.user.company
    )

    context = {
        'obj': compras
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

def almacen(request):

    pass

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
    compras = FacturaEnc.objects.filter(tipo="compra", empresa=request.user.company)
    ventas = FacturaEnc.objects.filter(tipo="factura", empresa=request.user.company)
    clientes = Cliente.objects.filter(empresa=request.user.company)
    proveedores = Proveedor.objects.filter(empresa=request.user.company)
    dcompras = FacturaEnc.objects.filter(tipo="compra",estado_pago='No Pagado', empresa=request.user.company)
    facturas = FacturaEnc.objects.filter(tipo="factura", estado_pago='No Pagado',empresa=request.user.company)

    facturas_year = get_total(facturas_year)
    compras_year = get_total(compras_year)
    facturas_mes = get_total(facturas_mes)
    compras_mes = get_total(compras_mes)

    ganancias_anual = facturas_year - compras_year
    ganancias_mensual = facturas_mes - compras_mes

    context = {
        'ventas_mes':f"${facturas_mes}",
        'ventas_anual':f"${facturas_year}",
        'ganancias_mensual':f"${ganancias_mensual}",
        'ganancias_anual':f"${ganancias_anual}",
        'compra':compras,
        'venta':ventas,
        'cliente':clientes,
        'proveedor':proveedores,
        'dcompras':dcompras,
        'facturas':facturas,
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

# Methods

def get_sum(data, field):

    if data.get(f'{field}__sum'):

        return data.get(f'{field}__sum')
    else:
        return 0
