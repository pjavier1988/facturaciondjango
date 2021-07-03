import datetime
import inv.views as inv
from django.db.models.aggregates import Sum
from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from bases.views import SinPrivilegios
from .models import Cliente, FacturaEnc, FacturaDet
from .forms import ClienteForm
from inv.models import Producto

class VistaBaseCreate(SuccessMessageMixin, SinPrivilegios, generic.CreateView):

    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):

    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

#Cliente ***************************************************************************************************************************************

class ClienteView(SinPrivilegios, generic.ListView):

    model = Cliente
    template_name = "fac/cliente_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_cliente"

    def get_queryset(self):
        
        if self.request.user.company:
            return Cliente.objects.filter(empresa = self.request.user.company)
        else:
            return None

class ClienteNew(VistaBaseCreate):

    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.add_cliente"

    def get(self, request, *args, **kwargs):
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})

class ClienteEdit(VistaBaseEdit):

    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"

    def get(self, request, *args, **kwargs):
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        print(form_class,form,context)
        return self.render_to_response(context)


@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

#Factura ***************************************************************************************************************************************

class FacturaView(SinPrivilegios, generic.ListView):

    model = FacturaEnc
    template_name = "fac/factura_list.html"
    context_object_name = "obj"
    permission_required="fac.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        #qs = super().get_queryset()
        if self.request.user.company:
            qs = FacturaEnc.objects.filter(empresa = self.request.user.company)
        else:
            qs = None

        if qs:

            for q in qs:
                print(q.uc,q.id)
        
            if not user.is_superuser:
                qs = qs.filter(uc=user,tipo='factura')
            else:
                qs = qs.filter(tipo='factura')

            for q in qs:
                print(q.uc,q.id)

            return qs
        else:
            return None

def getTransacciones(request):

    '''
    model = FacturaEnc
    template_name = "fac/transacciones_list.html"
    context_object_name = "obj"
    permission_required="fac.view_facturaenc"
    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs
        '''
        
    if request.method == 'GET':

        qs = FacturaEnc.objects.filter(empresa=request.user.company)
        total_compras = FacturaEnc.objects.filter(tipo='compra', empresa=request.user.company).aggregate(Sum('total'))
        total_ventas = FacturaEnc.objects.filter(tipo='factura', empresa=request.user.company).aggregate(Sum('total'))

        total_compras = get_total(total_compras)
        total_ventas = get_total(total_ventas)

        balance = total_ventas - total_compras

        context = {
            'obj': qs,
            'total_compras':total_compras,
            'total_ventas':total_ventas,
            'balance':balance
        }
        return render(request, 'fac/transacciones_list.html', context)


@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request,id=None):

    template_name='fac/facturas.html'
    detalle = {}
    clientes = Cliente.objects.filter(estado=True, empresa=request.user.company)
    
    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first()
        if id:
            if not enc:
                messages.error(request,'Factura No Existe')
                return redirect("fac:factura_list")

            usr = request.user
            if not usr.is_superuser:
                if enc.uc != usr:
                    messages.error(request,'Factura no fue creada por usuario')
                    return redirect("fac:factura_list")

        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0.00,
                'descuento':0.00,
                'faciva':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'faciva':enc.faciva,
                'total':enc.total
            }

        detalle=FacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        cli = Cliente.objects.get(pk=cliente)

        if not id:
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha,
                fecha_factura = fecha,
                fecha_compra = fecha,
                empresa = request.user.company,
                tipo = 'factura'
            )
            if enc:
                enc.save()
                id = enc.id
               
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = cli
                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("fac:factura_list")
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")

        prod = Producto.objects.get(codigo=codigo)

        det = FacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
            descuento = descuento,
            total = total,
            empresa = request.user.company,
        )
        
        if det:
            det.save()
        
        return redirect("fac:factura_edit",id=id)

    return render(request,template_name,contexto)


class ProductoView(inv.ProductoView):
    template_name="fac/buscar_producto.html" 

def borrar_detalle_factura(request, id):
    
    template_name = "fac/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user = authenticate(username=usr, password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)

def devolucion_facturas(request):

    template_name = 'fac/devolucion_facturas.html'

    clientes = Cliente.objects.filter(empresa = request.user.company)

    if request.method=='GET':

        context = {
            'obj': [],
            'clientes': clientes,
        }

        return render(request, template_name, context)

    if request.method=='POST':

        cliente = request.POST.get("cliente")
        fecha_max = request.POST.get("fecha-max")
        fecha_min = request.POST.get("fecha-min")
        facturas = {}

        if fecha_max and len(fecha_max) > 0:
            fecha_max = datetime.datetime.strptime(fecha_max.replace('-', '/'), '%Y/%m/%d')
        else:
            fecha_max = None

        if fecha_min and len(fecha_min) > 0:
            fecha_min = datetime.datetime.strptime(fecha_min.replace('-', '/'), '%Y/%m/%d')
        else:
            fecha_min = None

        if cliente and len(cliente) > 0:

            cliente = Cliente.objects.get(pk=cliente)

            if fecha_max and fecha_min:

                facturas = FacturaEnc.objects.filter(
                    tipo="factura",
                    empresa=request.user.company,
                    cliente=cliente,
                    fecha__range=[fecha_min, fecha_max],
                )

            elif fecha_max:

                facturas = FacturaEnc.objects.filter(
                    tipo="factura",
                    empresa=request.user.company,
                    cliente=cliente,
                    fecha__lte=fecha_max,
                )

            elif fecha_min:

                facturas = FacturaEnc.objects.filter(
                    tipo="factura",
                    empresa=request.user.company,
                    cliente=cliente,
                    fecha__gte=fecha_min,
                )

            else:

                facturas = FacturaEnc.objects.filter(
                    tipo="factura",
                    empresa=request.user.company,
                    cliente=cliente,
                )

        context = {
            'facturas': facturas,
            'clientes': clientes,
        }

        return render(request, template_name, context)

#Methods

def get_total(data):

    if data.get('total__sum'):

        return data.get('total__sum')
    else:
        return 0