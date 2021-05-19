from inv.models import Producto
from fac.models import FacturaEnc
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from datetime import datetime


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

    facturas_year = FacturaEnc.objects.filter(fecha__year=current_year,tipo="factura").aggregate(Sum('total'))
    compras_year = FacturaEnc.objects.filter(fecha__year=current_year,tipo="compra").aggregate(Sum('total'))
    facturas_mes = FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="factura").aggregate(Sum('total'))
    compras_mes = FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="compra").aggregate(Sum('total'))

    facturas_year = getTotal(facturas_year)
    compras_year = getTotal(compras_year)
    facturas_mes = getTotal(facturas_mes)
    compras_mes = getTotal(compras_mes)

    ganancias_anual = facturas_year - compras_year
    ganancias_mensual = facturas_mes - compras_mes
    productos = Producto.objects.filter(existencia__lte=5)

    contexto={
        'ventas_mes':f"${facturas_mes}",
        'ventas_anual':f"${facturas_year}",
        'ganancias_mensual':f"${ganancias_mensual}",
        'ganancias_anual':f"${ganancias_anual}",
        'obj':productos
    }

    return render(request,template_name,contexto)

class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):

    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"

#Methods

def getTotal(data):

    if data.get('total__sum'):

        return data.get('total__sum')
    else:
        return 0
