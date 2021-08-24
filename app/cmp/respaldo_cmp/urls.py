from .views import ProveedorEdit, ProveedorNew, ProveedorView, proveedor_inactivar
from django.urls import path

urlpatterns = [
    path('proveedores/new',ProveedorNew.as_view(),name="proveedor_new"),
    path('proveedores/',ProveedorView.as_view(),name="proveedor_list"),
    path('proveedores/edit/<int:pk>',ProveedorEdit.as_view(),name="proveedor_update"),
    path('proveedores/inactivar/<int:id>',proveedor_inactivar,name="proveedor_inactivar"),
]