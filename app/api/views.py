import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q, F, Count, Max
from django.db.models.aggregates import Sum
from .serializers import ProductoSerializer, CategoriaSerializer
from inv.models import Producto, Categoria
from fac.models import FacturaEnc, FacturaDet

#Productos Cliente *****************************************************************************************************************************

class ProductoList(APIView):

    def get(self,request):

        prod = Producto.objects.filter(empresa=request.user.company)
        data = ProductoSerializer(prod,many=True).data
        return Response(data)


class ProductoDetalle(APIView):
    
    def get(self,request, codigo):

        prod = get_object_or_404(Producto,Q(codigo=codigo)|Q(codigo_barras=codigo), empresa=request.user.company)
        data = ProductoSerializer(prod).data
        return Response(data)

class ProductosAgotados(APIView):

    def get(self, request):

        if request.user.company:
            productos = get_list_or_404(Producto, existencia__lt=F('min_stock'), empresa=request.user.company)
            return Response(data=ProductoSerializer(productos, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response()

#Gráficos **************************************************************************************************************************************

class Ganancias(APIView):

    def get(self, request):

        data = {}

        if request.user.company:
            
            year = self.request.query_params.get('year')
            month = self.request.query_params.get('month')
            date = datetime.datetime.now()

            if not year and not len(str(year)) > 0:
                year = date.year

            if not month and not len(str(month)) > 0:
                data = get_ganancias_mensuales(request, int(year))
            else:
                data = get_ganancias_mes(request, int(year), int(month))

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response()

class Ventas(APIView):

    def get(self, request):

        if request.user.company:
            
            year = self.request.query_params.get('year')
            month = self.request.query_params.get('month')
            date = datetime.datetime.now()

            if not year and not len(str(year)) > 0:
                year = date.year

            if not month and not len(str(month)) > 0:
                data = get_ventas_mensuales(request, int(year))
            else:
                data = get_ventas_mes(request, int(year), int(month))

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response()

class ProductosVendidos(APIView):

    def get(self, request):

        if request.user.company:
            
            year = self.request.query_params.get('year')
            month = self.request.query_params.get('month')
            date = datetime.datetime.now()

            if not year and not len(str(year)) > 0:
                year = date.year

            if not month and not len(str(month)) > 0:
                data = get_productos_v_mensuales(request, int(year))
            else:
                data = get_productos_v_mes(request, int(year), int(month))

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response()

class ProductosAnual(APIView):

    def get(self, request):

        if request.user.company:
            
            products = self.request.query_params.get('products')
            year = self.request.query_params.get('year')
            date = datetime.datetime.now()

            if not year and not len(str(year)) > 0:
                year = date.year

            if products and len(products) > 0:

                data = get_comparacion_productos(request, products, year)
                return Response(data=data, status=status.HTTP_200_OK)

            data = get_productos_anual(request, int(year))
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

#Productos ******************************************************************************************************************************

class ProductosByIds(APIView):

    def get(self, request):

        if request.user.company:

            products = self.request.query_params.get('products')

            if products and len(products) > 0:

                products = products.split(',')
                product_list = []

                for p in products:

                    producto = Producto.objects.filter(pk=int(p)).first()

                    if producto:
                        product_list.append(producto)

                if len(product_list) > 0:
                    return Response(data=ProductoSerializer(product_list, many=True).data, status=status.HTTP_200_OK)
                else:
                    return Response(data=None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)


#Categorias *****************************************************************************************************************************

class CategoriaList(APIView):

    def get(self, request):

        categorias = Categoria.objects.all()
        data = CategoriaSerializer(categorias, many=True).data
        return Response(data)

#Methods Ganancias

def get_ganancias_mensuales(request, year):

    data = {}

    for i in range(12):

        i = i + 1
 
        facturas_mes = FacturaEnc.objects.filter(
            fecha__year=year,
            fecha__month=i,
            tipo="factura",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        compras_mes = FacturaEnc.objects.filter(
            fecha__year=year,
            fecha__month=i,
            tipo="compra",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        ganancia = get_total(facturas_mes) - get_total(compras_mes)
        date = datetime.datetime(year, i, 1)
        data[str(date.strftime('%B'))] = ganancia

    return data

def get_ganancias_mes(request, year, month):

    data = {}
    
    for i in range(get_dias_del_mes(month, year)):

        i = i+1

        facturas = FacturaEnc.objects.filter(
            fecha__year=year,
            fecha__month=month,
            fecha__day=i,
            tipo="factura",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        compras = FacturaEnc.objects.filter(
            fecha__year=year,
            fecha__month=month,
            fecha__day=i,
            tipo="compra",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        date = datetime.datetime(year, month, i)
        data[f'{date.strftime("%B")} - {date.day}'] = get_total(facturas) - get_total(compras)

    return data

#Methods Ventas

def get_ventas_mensuales(request, year):

    data = {}

    for i in range(12):

        i = i + 1

        facturas_mes = FacturaEnc.objects.filter(
            fecha__year=year,
            fecha__month=i,
            tipo="factura",
            empresa=request.user.company).count()

        date = datetime.datetime(year, i, 1)
        data[str(date.strftime('%B'))] = facturas_mes

    return data
        
def get_ventas_mes(request, year, month):

    data = {}

    for i in range(get_dias_del_mes(month, year)):

        i = i + 1

        facturas = FacturaEnc.objects.filter(
            fecha__year=year,
            fecha__month=month,
            fecha__day=i,
            tipo="factura",
            empresa=request.user.company).count()

        date = datetime.datetime(year, month, i)
        data[f'{date.strftime("%B")} - {date.day}'] = facturas

    return data

def get_productos_v_mensuales(request, year):

    data = {}

    for i in range(12):

        i = i +1

        facturas = FacturaDet.objects.filter(
            factura__fecha__year=year,
            factura__fecha__month=i,
            factura__tipo="factura",
            empresa=request.user.company).values('producto__descripcion').order_by('-producto__count').annotate(Count('producto')).first()

        date = datetime.datetime(year, i, 1)

        if facturas:
            data[f'{str(date.strftime("%B"))} - {facturas.get("producto__descripcion")}'] = facturas.get('producto__count')
        else:
            data[str(date.strftime('%B'))] = 0

    return data

def get_productos_v_mes(request, year, month):

    data = {}

    for i in range(get_dias_del_mes(month, year)):

        i = i + 1

        facturas = FacturaDet.objects.filter(
            factura__fecha__year=year,
            factura__fecha__month=month,
            factura__tipo="factura",
            factura__fecha__day=i,
            empresa=request.user.company).values('producto__descripcion').order_by('-producto__count').annotate(Count('producto')).first()        

        date = datetime.datetime(year, month, i)
        
        if facturas:
            data[f'{date.day} - {facturas.get("producto__descripcion")}'] = facturas.get('producto__count')
        else:
            data[f'{str(date.strftime("%B"))} {date.day}'] = 0

    return data

def get_productos_anual(request, year):

    data = {}

    facturas = FacturaDet.objects.filter(
        factura__fecha__year=year,
        factura__tipo="factura",
        empresa=request.user.company).values('producto__descripcion').order_by('-producto__count').annotate(Count('producto'))[:10]

    total = 0
    for f in facturas:
        total = total + f.get('producto__count')

    for f in facturas:
        
        result = round((f.get('producto__count') * 100) / total)
        data[f.get('producto__descripcion')] = result

    return data

def get_comparacion_productos(request, products: str, year):

    data = {}
    products = products.split(',')
    acum = []
    total = 0

    for p in products:

        producto = Producto.objects.filter(pk=int(p)).first()

        if producto:
            facturas = FacturaDet.objects.filter(
                factura__fecha__year=year,
                factura__tipo="factura",
                producto=producto,
                empresa=request.user.company).values('producto__descripcion').order_by('-producto__count').annotate(Count('producto'))

            if facturas:
                acum.append(facturas[0])

    if len(acum) > 0:

        for fac in acum:
            total = total + fac.get('producto__count')

        for fac in acum:
            result = round((fac.get('producto__count') * 100) / total)
            data[fac.get('producto__descripcion')] = result
    
    return data
    
#Methods

def get_total(data):

    if data.get('total__sum'):

        return data.get('total__sum')
    else:
        return 0

def es_bisiesto(anio: int) -> bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def get_dias_del_mes(mes: int, anio: int) -> int:
    if mes in [4, 6, 9, 11]:
        return 30
    if mes == 2:
        if es_bisiesto(anio):
            return 29
        else:
            return 28
    else:
        return 31