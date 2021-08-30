from django.urls import path, include
from .views import ProductoList, ProductoDetalle, ProductosAgotados, Ganancias, Ventas, CategoriaList, ProductosVendidos, ProductosAnual, ProductosByIds

urlpatterns = [
    path('v1/productos/',ProductoList.as_view(),name='producto_list'),
    path('v1/productos/<str:codigo>',ProductoDetalle.as_view(),name='producto_detalle'),
    path('v1/productos/agotados/', ProductosAgotados.as_view(), name='producto_agotado'),
    path('v1/productos/vendidos/anual', ProductosAnual.as_view(), name='productos_anual'),
    path('v1/productos/by/string/ids', ProductosByIds.as_view(), name='productos_ids'),
    
    #Gráficos
    path('v1/facturas/ganancias/mensuales', Ganancias.as_view(), name='ganancias'),
    path('v1/facturas/ventas/mensuales', Ventas.as_view(), name='ventas'),
    path('v1/productos/mas/vendidos', ProductosVendidos.as_view(), name='productos_vendidos'),

    path('v1/categorias/all', CategoriaList.as_view(), name='categoria_list'),
]