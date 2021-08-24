import datetime
import json
from fac.models import FacturaDet
from fac.models import FacturaEnc
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Sum
from .models import Proveedor, ComprasEnc, ComprasDet
from cmp.forms import ProveedorForm,ComprasEncForm
from bases.views import SinPrivilegios
from inv.models import Producto

#Proveedor **************************************************************************************************************************************

class ProveedorView(SinPrivilegios, generic.ListView):

    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_proveedor"

    def get_queryset(self):
        
        if self.request.user.company:
            return Proveedor.objects.filter(empresa = self.request.user.company)
        else:
            return None

class ProveedorNew(SuccessMessageMixin, SinPrivilegios, generic.CreateView):

    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo"
    permission_required="cmp.add_proveedor"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        #print(self.request.user.id)
        return super().form_valid(form)


class ProveedorEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):

    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Editado"
    permission_required="cmp.change_proveedor"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


@login_required(login_url="/login/")
@permission_required("cmp.change_proveedor",login_url="/login/")
def proveedorInactivar(request,id):

    template_name='cmp/inactivar_prv.html'
    contexto={}
    prv = Proveedor.objects.filter(pk=id).first()

    if not prv:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':prv}

    if request.method=='POST':
        prv.estado=False
        prv.save()
        contexto={'obj':'OK'}
        
        return HttpResponse('Proveedor desactivado')

    return render(request,template_name,contexto)

#Compras ***************************************************************************************************************************************

class ComprasView(SinPrivilegios, generic.ListView):

    model = FacturaEnc
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_comprasenc"

    def get_queryset(self):

        user = self.request.user
        # print(user,"usuario")
        
        if self.request.user.company:
            qs = FacturaEnc.objects.filter(empresa = self.request.user.company)
        else:
            qs = None

        #qs = super().get_queryset()

        if qs:            
            for q in qs:
                print(q.uc,q.id)
        
            if not user.is_superuser:
                qs = qs.filter(uc=user,tipo='compra')
            else:
                qs = qs.filter(tipo='compra')

            for q in qs:    
                print(q.uc,q.id)

            return qs
        else:
            return None


@login_required(login_url='/login/')
@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):

    template_name = "cmp/compras.html"
    prod = Producto.objects.filter(estado=True,es_servicio=False, empresa=request.user.company)
    form_compras = {}
    contexto = {}

    if request.method == 'GET':

        form_compras = ComprasEncForm(request.user)
        enc = FacturaEnc.objects.filter(pk=compra_id).first()

        if enc:

            det = FacturaDet.objects.filter(factura=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra':fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total':enc.total
            }
            form_compras = ComprasEncForm(request.user, e)
        else:
            det=None
        
        contexto={'productos':prod,'encabezado':enc,'detalle':det,'form_enc':form_compras}

    if request.method=='POST':

        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:

            prov=Proveedor.objects.get(pk=proveedor)

            enc = FacturaEnc(
                fecha_compra = fecha_compra,
                observacion = observacion,
                no_factura = no_factura,
                fecha_factura = fecha_factura,
                proveedor = prov,
                uc = request.user,
                empresa = request.user.company,
                tipo = 'compra' 
            )
            if enc:
                enc.save()
                compra_id = enc.id
        else:

            enc = FacturaEnc.objects.filter(pk=compra_id).first()

            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.no_factura = no_factura
                enc.fecha_factura = fecha_factura
                enc.um = request.user.id
                enc.save()

        if not compra_id:

            return redirect("cmp:compras_list")
        
        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle  = request.POST.get("id_descuento_detalle")
        total_detalle  = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = FacturaDet(

            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio_prv = precio,
            descuento = descuento_detalle,
            costo = 0,
            uc = request.user,
            empresa = request.user.company
        )

        if det:

            det.save()

            sub_total = FacturaDet.objects.filter(factura=compra_id).aggregate(Sum('sub_total'))
            descuento = FacturaDet.objects.filter(factura=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento = descuento["descuento__sum"]

            enc.save()

        return redirect("cmp:compras_edit",compra_id=compra_id)


    return render(request, template_name, contexto)


class CompraDetDelete(SinPrivilegios, generic.DeleteView):

    permission_required = "cmp.delete_comprasdet"
    model = ComprasDet
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
          compra_id=self.kwargs['compra_id']
          return reverse_lazy('cmp:compras_edit', kwargs={'compra_id': compra_id})

def devolucion_compras(request):

    template_name = 'cmp/devolucion_compras.html'

    proveedores = Proveedor.objects.filter(empresa = request.user.company)

    if request.method=='GET':

        context = {
            'obj': [],
            'proveedores': proveedores,
        }

        return render(request, template_name, context)

    if request.method=='POST':

        proveedor = request.POST.get("proveedor")
        fecha_max = request.POST.get("fecha-max")
        fecha_min = request.POST.get("fecha-min")
        compras = {}

        if fecha_max and len(fecha_max) > 0:
            fecha_max = datetime.datetime.strptime(fecha_max.replace('-', '/'), '%Y/%m/%d')
        else:
            fecha_max = None

        if fecha_min and len(fecha_min) > 0:
            fecha_min = datetime.datetime.strptime(fecha_min.replace('-', '/'), '%Y/%m/%d')
        else:
            fecha_min = None

        if proveedor and len(proveedor) > 0:

            proveedor = Proveedor.objects.get(pk=proveedor)

            if fecha_max and fecha_min:

                compras = FacturaEnc.objects.filter(
                    tipo="compra",
                    empresa=request.user.company,
                    proveedor=proveedor,
                    fecha__range=[fecha_min, fecha_max],
                )

            elif fecha_max:

                compras = FacturaEnc.objects.filter(
                    tipo="compra",
                    empresa=request.user.company,
                    proveedor=proveedor,
                    fecha__lte=fecha_max,
                )

            elif fecha_min:

                compras = FacturaEnc.objects.filter(
                    tipo="compra",
                    empresa=request.user.company,
                    proveedor=proveedor,
                    fecha__gte=fecha_min,
                )

            else:

                compras = FacturaEnc.objects.filter(
                    tipo="compra",
                    empresa=request.user.company,
                    proveedor=proveedor,
                )



        context = {
            'compras': compras,
            'proveedores': proveedores,
        }

        return render(request, template_name, context)

def devolver(request, factura_id, template):

    factura = FacturaEnc.objects.get(pk=factura_id)
    factura.estado_pago = 'No Pagado'
    factura.save()

    return redirect(f'{template}')

def pagar(request, factura_id, template):

    factura = FacturaEnc.objects.get(pk=factura_id)
    factura.estado_pago = 'Pagado'
    factura.save()

    return redirect(f'{template}')