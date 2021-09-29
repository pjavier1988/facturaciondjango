from django.urls import path
from .views import CategoriaView,CategoriaNew,CategoriaEdit,CategoriaDelete, ProductoEdit, ProductoNew, ProductoView, SubCategoriaView,\
    SubCategoriaNew,SubCategoriaEdit,SubCategoriaDelete,MarcaView,MarcaNew,MarcaEdit, UnidadMedidaEdit, UnidadMedidaNew, UnidadMedidaView,marca_inactivar, producto_inactivar, unidadmedida_inactivar, perdidas

urlpatterns = [
    path('categorias/new',CategoriaNew.as_view(),name="categoria_new"),
    path('categorias/',CategoriaView.as_view(),name="categoria_list"),
    path('categorias/edit/<int:pk>',CategoriaEdit.as_view(),name="categoria_update"),
    path('categorias/delete/<int:pk>',CategoriaDelete.as_view(),name="categoria_del"),

    path('subcategorias/',SubCategoriaView.as_view(),name="subcategoria_list"),
    path('subcategorias/new',SubCategoriaNew.as_view(),name="subcategoria_new"),
    path('subcategorias/edit/<int:pk>',SubCategoriaEdit.as_view(),name="subcategoria_update"),
    path('subcategorias/delete/<int:pk>',SubCategoriaDelete.as_view(),name="subcategoria_del"),

    path('marcas/',MarcaView.as_view(),name="marca_list"),
    path('marcas/new',MarcaNew.as_view(),name="marca_new"),
    path('marcas/edit/<int:pk>',MarcaEdit.as_view(),name="marca_update"),
    path('marcas/inactivar/<int:id>',marca_inactivar,name="marca_inactivar"),

    path('unidadesmedida/',UnidadMedidaView.as_view(),name="unidadmedida_list"),
    path('unidadesmedida/new',UnidadMedidaNew.as_view(),name="unidadmedida_new"),
    path('unidadesmedida/edit/<int:pk>',UnidadMedidaEdit.as_view(),name="unidadmedida_update"),
    path('unidadesmedida/inactivar/<int:id>',unidadmedida_inactivar,name="unidadmedida_inactivar"),

    path('productos/',ProductoView.as_view(),name="producto_list"),
    path('productos/new',ProductoNew.as_view(),name="producto_new"),
    path('productos/edit/<int:pk>',ProductoEdit.as_view(),name="producto_update"),
    path('productos/inactivar/<int:id>',producto_inactivar,name="producto_inactivar"),
    path('perdidas/', perdidas, name='perdidas'),
]
