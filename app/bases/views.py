from inv.models import Producto
from fac.models import FacturaEnc
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
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
    #template_name = 'bases/home.html'
    #login_url='bases:login'
    template_name='bases/home.html'
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    print(f"MES ACTUAL {current_month}")
    facturasAnio=FacturaEnc.objects.filter(fecha__year=current_year,tipo="factura").aggregate(Sum('total'))
    comprasAnio=FacturaEnc.objects.filter(fecha__year=current_year,tipo="compra").aggregate(Sum('total'))
    ganancias_anual = facturasAnio.get('total__sum') -comprasAnio.get('total__sum')
    #facturasMes=FacturaEnc.objects.filter(fecha__month=4,tipo="factura").aggregate(Sum('total'))
    fechagte=datetime(current_year, current_month, 1)
    next_month = current_month+1
    if(next_month==13):
        next_month=1
    
    fechalte=datetime(current_year, next_month, 1)
    facturasMes=FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="factura").aggregate(Sum('total'))
    comprasMes=FacturaEnc.objects.filter(fecha__gte=fechagte,fecha__lte=fechalte,tipo="compra").aggregate(Sum('total'))
    ganancias_mensual = facturasMes.get('total__sum') -comprasMes.get('total__sum')
    totalFacturasMes= facturasMes.get('total__sum');
    totalComprasMes= comprasMes.get('total__sum');
    if totalFacturasMes is not None:
        print("entre a None facturaMes")
        print(facturasMes)
        totalFacturasMes = facturasMes.get('total__sum')
    else:
        totalFacturasMes = 0

    if totalComprasMes is not None:
        print("entre a None comprasMes")
        print(comprasMes)
        totalComprasMes = comprasMes.get('total__sum')
    else:
        totalComprasMes = 0

    ganancias_mensual = totalFacturasMes - totalComprasMes

    productos = Producto.objects.filter(existencia__lte=5)
    print(f"MES {facturasMes}")
    #print(f"facturas {facturasMes}")
    contexto={
        'ventas_mes':f"${ganancias_mensual}",
        'ventas_anual':f"${facturasAnio.get('total__sum')}",
        'ganancias_mensual':f"${ganancias_mensual}",
        'ganancias_anual':f"${ganancias_anual}",
        'obj':productos

    }

    return render(request,template_name,contexto)


class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"
