import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q, F
from django.db.models.aggregates import Sum
from .serializers import ProductoSerializer, CategoriaSerializer
from inv.models import Producto, Categoria
from fac.models import FacturaEnc

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

    def get(self, request, intervalo):

        if request.user.company:

            if intervalo == 1:
                data = get_ganancias_mensuales(request)
            elif intervalo == 2:
                data = get_ganancias_mes(request)
            elif intervalo == 3:
                print (intervalo)

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response()

class Ventas(APIView):

    def get(self, request, intervalo):

        if request.user.company:

            if intervalo == 1:
                data = get_ventas_mensuales(request)
            elif intervalo == 2:
                data = get_ventas_mes(request)
            elif intervalo == 3:
                print (intervalo)

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response()

class ProductosVendidos(APIView):

    def get(self, request, intervalo):

        if request.user.company:

            if intervalo == 1:
                data = get_ventas_mensuales(request)
            elif intervalo == 2:
                data = get_ventas_mes(request)
            elif intervalo == 3:
                print (intervalo)

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response()

#Catalogos ***************************************************************************************************************************************

class CategoriaList(APIView):

    def get(self, request):

        categorias = Categoria.objects.all()
        data = CategoriaSerializer(categorias, many=True).data
        return Response(data)

#Methods Ganancias

def get_ganancias_mensuales(request):

    data = {}
    date = datetime.datetime.now()

    for _ in range(12):

        facturas_mes = FacturaEnc.objects.filter(
            fecha__year=date.year,
            fecha__month=date.month,
            tipo="factura",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        compras_mes = FacturaEnc.objects.filter(
            fecha__year=date.year,
            fecha__month=date.month,
            tipo="compra",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        ganancia = get_total(facturas_mes) - get_total(compras_mes)
        data[str(date.strftime('%B'))] = ganancia
        date = date + relativedelta(months=-1)

    return data

def get_ganancias_mes(request):

    data = {}
    date = datetime.datetime.now()
    
    for _ in range(get_dias_del_mes(date.month, date.year)):

        facturas = FacturaEnc.objects.filter(
            fecha__year=date.year,
            fecha__month=date.month,
            fecha__day=date.day,
            tipo="factura",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        compras = FacturaEnc.objects.filter(
            fecha__year=date.year,
            fecha__month=date.month,
            fecha__day=date.day,
            tipo="compra",
            empresa=request.user.company
        ).aggregate(Sum('total'))

        data[f'{date.strftime("%B")} - {date.day}'] = get_total(facturas) - get_total(compras)
        date = date + relativedelta(days=-1)

    return data

#Methods Ventas

def get_ventas_mensuales(request):

    data = {}
    date = datetime.datetime.now()

    for _ in range(12):

        facturas_mes = FacturaEnc.objects.filter(
            fecha__year=date.year,
            fecha__month=date.month,
            tipo="factura",
            empresa=request.user.company).count()

        data[str(date.strftime('%B'))] = facturas_mes
        date = date + relativedelta(months=-1)

    return data
        
def get_ventas_mes(request):

    data = {}
    date = datetime.datetime.now()

    for _ in range(get_dias_del_mes(date.month, date.year)):

        facturas = FacturaEnc.objects.filter(
            fecha__year=date.year,
            fecha__month=date.month,
            fecha__day=date.day,
            tipo="factura",
            empresa=request.user.company).count()

        data[f'{date.strftime("%B")} - {date.day}'] = facturas
        date = date + relativedelta(days=-1)

    return data

#Methods Productos Vendidos

def get_productos_v_mensuales(request):

    print('')
    
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