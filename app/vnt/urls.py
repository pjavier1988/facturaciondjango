from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .reportes import imprimir_cotizacion, detalle_cotizacion

urlpatterns = [
    path('home',views.home, name='home'),
    path('productos/by/categoria/<int:id>',views.ProductosByCategoria.as_view(), name='productos_categoria'),
    path('productos/en/oferta', views.ProductosOferta.as_view(), name='productos_oferta'),
    path('productos/detail/<int:pk>', views.ProductoDetail.as_view(), name="producto_det"),
    path('productos/search', views.SearchProduct.as_view(), name="producto_search"),

    path('cart/insert/<int:producto_id>/<str:template_name>', views.insert_product, name='insert_product'),
    path('cart/remove/<int:producto_id>/<str:template_name>', views.remove_product, name='remove_product'),
    path('cart/decrement/<int:producto_id>/<str:template_name>', views.decrement_product, name='decrement_product'),
    path('cart/clear/<str:template_name>', views.clear_cart, name='clear_cart'),
    path('cotizacion/lista', views.cotizacion_list, name='cotizacion_list'),
    path('cotizacion/PDF/<int:id>', imprimir_cotizacion, name='cotizacion_print'),
    path('cotizacion/detalle/<int:id>', detalle_cotizacion, name='detalle_cotizacion'),
    path('cotización/delete/<int:id>', views.cotizacion_delete, name='delete_cotizacion'),
    path('cotizacion/new',views.cotizacion_new,name="cotizacion_form"),
]
