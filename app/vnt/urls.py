from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, ProductosByCategoria, ProductosOferta, ProductoDetail, SearchProduct
from . import views

urlpatterns = [
    path('home',home, name='home'),
    path('productos/by/categoria/<int:id>', ProductosByCategoria.as_view(), name='productos_categoria'),
    path('productos/en/oferta', ProductosOferta.as_view(), name='productos_oferta'),
    path('productos/detail/<int:pk>', ProductoDetail.as_view(), name="producto_det"),
    path('productos/search', SearchProduct.as_view(), name="producto_search"),

    path('cart/insert/<int:producto_id>/<str:template_name>', views.insert_product, name='insert_product'),
    path('cart/remove/<int:producto_id>/<str:template_name>', views.remove_product, name='remove_product'),
    path('cart/decrement/<int:producto_id>/<str:template_name>', views.decrement_product, name='decrement_product'),
    path('cart/clear/<str:template_name>', views.clear_cart, name='clear_cart'),
]