from inv.models import Producto, Categoria
from fac.models import FacturaEnc
from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from datetime import datetime

def validar_usuario(request):
    if request.user.is_authenticated:
      if request.user.groups.name  == "Client":
        return redirect('vnt:home')
      elif request.user.groups.name == "Mod":
        return redirect('base:home')
      elif request.user.is_admin:
        return redirect('/admin/')
    return redirect('/login/')

class MixinFormInvalid:

    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):

    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

@login_required(login_url='/login/')
@permission_required('cmp.view_comprasenc', login_url='bases:login')
def Home(request):

    template_name='bases/home.html'

    current_year = datetime.now().year
    current_month = datetime.now().month
    fechagte=datetime(current_year, current_month, 1)
    next_month = current_month + 1

    if(next_month==13):
        next_month=1
    
    fechalte=datetime(current_year, next_month, 1)

    facturas_year = FacturaEnc.objects.filter(fecha__year=current_year,tipo="factura", empresa=request.user.company).aggregate(Sum('total'))
    compras_year = FacturaEnc.objects.filter(fecha__year=current_year,tipo="compra", empresa=request.user.company).aggregate(Sum('total'))
    facturas_mes = FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="factura", empresa=request.user.company).aggregate(Sum('total'))
    compras_mes = FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="compra", empresa=request.user.company).aggregate(Sum('total'))

    facturas_year = get_total(facturas_year)
    compras_year = get_total(compras_year)
    facturas_mes = get_total(facturas_mes)
    compras_mes = get_total(compras_mes)

    ganancias_anual = facturas_year - compras_year
    ganancias_mensual = facturas_mes - compras_mes
    productos = Producto.objects.filter(existencia__lte=5, empresa=request.user.company)

    contexto={
        'ventas_mes':f"${facturas_mes}",
        'ventas_anual':f"${facturas_year}",
        'ganancias_mensual':f"${ganancias_mensual}",
        'ganancias_anual':f"${ganancias_anual}",
        'categorias_productos': get_products_and_category(request),
        'obj':productos,
    }

    return render(request,template_name,contexto)

class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):

    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"

#Methods

def get_total(data):

    if data.get('total__sum'):

        return data.get('total__sum')
    else:
        return 0

def get_products_and_category(request):

    data = {}

    categorias = Categoria.objects.all()
    print (Categoria)
    print ('****************************************************')

    for c in categorias:

        productos = Producto.objects.filter(subcategoria__categoria=c, empresa=request.user.company)

        if productos:
            data[c.descripcion] = productos
    
    return data