from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from .models import Cotizacion, ProductosCotizacion
from .forms import CotizacionForm
from .cart import Cart
from .models import *
from inv.models import Producto, Categoria, SubCategoria
from fac.models import Cliente, FacturaEnc, FacturaDet
from bases.views import get_products_and_category
from fac.models import FacturaEnc, Cliente, FacturaDet
from param.models import Links
import datetime

TEMPLATE_USER_HOME = 'vnt/home.html'

def home(request):

    template_name = TEMPLATE_USER_HOME
    productos = list(Producto.objects.filter(existencia__gte=0))

    nuevos = []
    populares = []

    for _ in range(4):
        obj_max_date = get_obj_by_max_date(productos)
        nuevos.append(obj_max_date)
        productos.remove(obj_max_date)

    populares = productos
    
    imagenes = Links.objects.filter(
        empresa=request.user.company,
        plataforma='Carousel',
        estado=1,
    )[:8]

    context = {
        'imagenes': imagenes,
        'carousel': True,
        'sections': {
            'nuevos': nuevos,
            'populares': populares
        },
    }

    return render(request, template_name, context)

class ProductosByCategoria(generic.TemplateView):

    template_name = 'vnt/productos_categoria.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categoria = Categoria.objects.filter(pk=self.kwargs['id']).first()
        subcategorias = SubCategoria.objects.filter(categoria=categoria)
        productos = Producto.objects.filter(subcategoria__categoria=categoria)

        context['categoria'] = categoria
        context['subcategorias'] = subcategorias
        context['obj'] = productos

        return context

class ProductosOferta(generic.TemplateView):

    template_name = TEMPLATE_USER_HOME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        productos = list(Producto.objects.filter(existencia__gte=0))

        context['carousel'] = False
        context['sections'] = {
            'En oferta': productos,
            'Con descuentos': productos,
        }

        return context

class ProductoDetail(generic.DetailView):

    model = Producto
    template_name = "vnt/producto_detail.html"
    context_object_name = "obj"

class SearchProduct(generic.TemplateView):

    template_name = TEMPLATE_USER_HOME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        desc = self.request.GET.get('desc')
        categorias = self.request.GET.get('categorias')
        subcategorias = self.request.GET.get('subcategorias')

        if categorias and len(categorias) > 0:

            categoria = Categoria.objects.filter(pk=categorias).first()
            resultados = list(Producto.objects.filter(
                Q(descripcion__contains=desc.upper()) &
                Q(subcategoria__categoria=categoria))[:4])
            similares = get_similares(resultados, self.request)

        elif subcategorias and len(subcategorias) > 0:

            subcategoria = SubCategoria.objects.filter(pk=subcategorias).first()
            resultados = list(Producto.objects.filter(
                Q(descripcion__contains=desc.upper()) &
                Q(subcategoria=subcategoria))[:4])
            similares = get_similares(resultados, self.request)

        else:
            resultados = list(Producto.objects.filter(Q(descripcion__contains=desc.upper()))[:4])
            similares = get_similares(resultados, self.request)

        context['carousel'] = False
        context['sections'] = {
            'resultados': resultados,
            'relacionados': similares,
        }

        return context

#Carrito ***************************************************************************************************************************************

def insert_product(request, producto_id, template_name):

    cart = Cart(request)
    producto = Producto.objects.get(id=producto_id)
    cart.add(producto)

    categoria_id = request.GET.get("categoria_id")

    if categoria_id:
        return redirect(f'vnt:{template_name}', id=categoria_id)
    else:
        return redirect(f'vnt:{template_name}')

def remove_product(request, producto_id, template_name):

    cart = Cart(request)
    producto = Producto.objects.get(id=producto_id)
    cart.remove(producto)

    categoria_id = request.GET.get("categoria_id")

    if categoria_id:
        return redirect(f'vnt:{template_name}', id=categoria_id)
    else:
        return redirect(f'vnt:{template_name}')

def decrement_product(request, producto_id, template_name):

    cart = Cart(request)
    producto = Producto.objects.get(id=producto_id)
    cart.decrement(producto)

    categoria_id = request.GET.get("categoria_id")

    if categoria_id:
        return redirect(f'vnt:{template_name}', id=categoria_id)
    else:
        return redirect(f'vnt:{template_name}')

def clear_cart(request, template_name):

    cart = Cart(request)
    cart.clear()

    categoria_id = request.GET.get("categoria_id")

    if categoria_id:
        return redirect(f'vnt:{template_name}', id=categoria_id)
    else:
        return redirect(f'vnt:{template_name}')

# Cotización *****************************************************************************************************************************

@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def cotizacion_new(request):

    template_name = "vnt/cotizacion_form.html"
    clientes = Cliente.objects.filter(estado=True, empresa=request.user.company)

    if request.method=='GET':

        context = {
            'clientes': clientes,
            'categorias_productos': get_products_and_category(request),
        }

        return render(request, template_name, context)

    if request.method=='POST':

        cliente_id = request.POST.get("cliente")
        fecha = request.POST.get("fecha")
        impuestos = request.POST.get("impuestos")
        descuento = request.POST.get("descuento")
        envio = request.POST.get("envio")
        estado = request.POST.get("estado")
        nota = request.POST.get("nota")
        products = request.POST.get('product-ids')

        cliente = Cliente.objects.get(pk=cliente_id)

        cotizacion = Cotizacion(
            cliente = cliente,
            estado_cotizacion = estado,
            iva = impuestos,
            descuento = descuento,
            envio = envio,
            nota = nota,
            uc = request.user,
            empresa = request.user.company,
        )

        cotizacion.save()
        cotizacion = Cotizacion.objects.latest('fc')

        if products and len(products) > 0:

            products = products.split(',')

            for p in products:

                producto = Producto.objects.filter(pk=int(p)).first()

                if producto:

                    productos_cotizacion = ProductosCotizacion(
                        cotizacion = cotizacion,
                        producto = producto,
                        cantidad = 1,
                        uc = request.user,
                    )

                    productos_cotizacion.save()

        return redirect('inv:categoria_list')

def cotizacion_list(request):
    template_name = 'vnt/cotizacion_list.html'

    cotizacion = Cotizacion.objects.filter(
        estado = 1,
        empresa = request.user.company,
    )
    context = {
        'obj':cotizacion
    }
    return render(request, template_name, context)

def cotizacion_delete(request, id):

    template_name = 'vnt/cotizacion_list.html'
    cotizacion = Cotizacion.objects.get(id = id)
    cotizacion.estado = 0
    cotizacion.save()
    cotizacionlist = Cotizacion.objects.filter(
        estado = 1,
        empresa = request.user.company,
    )

    context = {
        'obj':cotizacionlist
    }

    return render(request, template_name, context)

def convertir_a_factura(request, cot_id):

    cotizacion = Cotizacion.objects.get(id=cot_id)
    productos = ProductosCotizacion.objects.filter(
        cotizacion=cotizacion,
    )

    enc = FacturaEnc(
        cliente=cotizacion.cliente,
        fecha=datetime.datetime.now(),
        sub_total=cotizacion.sub_total,
        faciva=cotizacion.iva,
        descuento=cotizacion.descuento,
        total=cotizacion.total,
        fecha_factura=datetime.datetime.now(),
        fecha_compra=datetime.datetime.now(),
        tipo='factura',
        estado_pago='Pagado',
        empresa=request.user.company,
        uc=request.user,
    )

    enc.save()

    if enc.id:

        for p in productos:

            det = FacturaDet(
                factura=enc,
                producto=p.producto,
                cantidad=p.cantidad,
                precio=p.producto.precio,
                descuento=p.descuento,
                precio_prv=p.producto.precio,
                costo=p.producto.precio,
                empresa=request.user.company,
                uc=request.user,
            )

            det.save()

    return redirect('param:ventas_list')

#Methods

def get_obj_by_max_date(objects):

    obj = None

    for o in objects:
        if obj == None:
            obj = o
        else:
            if obj.fc < o.fc:
                obj = o

    return obj

def get_similares(resultados, request):

    if resultados:
        similares = list(Producto.objects.filter(
            subcategoria=resultados[0].subcategoria,
            empresa=request.user.company,
        )[:4])

        for r in resultados:
            similares.remove(r)

        return similares
    else:
        return None
