from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import ProductoSerializer
from inv.models import Producto
from django.db.models import Q, F

class ProductoList(APIView):
    def get(self,request):
        prod = Producto.objects.all()
        data = ProductoSerializer(prod,many=True).data
        return Response(data)


class ProductoDetalle(APIView):
    def get(self,request, codigo):
        prod = get_object_or_404(Producto,Q(codigo=codigo)|Q(codigo_barras=codigo))
        data = ProductoSerializer(prod).data
        return Response(data)

class ProductosAgotados(APIView):

    def get(self, request):

        #productos = Producto.objects.filter(existencia__lt=F('min_stock'))
        productos = get_list_or_404(Producto, existencia__lt=F('min_stock'))
        return Response(data=ProductoSerializer(productos, many=True).data)