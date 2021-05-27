from django.urls import path, include
from .views import ProductoList, ProductoDetalle, ProductosAgotados

urlpatterns = [
    path('v1/productos/',ProductoList.as_view(),name='producto_list'),
    path('v1/productos/<str:codigo>',ProductoDetalle.as_view(),name='producto_detalle'),
    path('v1/productos/agotados/', ProductosAgotados.as_view(), name='producto_agotado')
]