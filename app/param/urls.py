from django.urls import path
from .views import EmpresaDet, EmpresaNew, EmpresaEdit
from . import views
from . import reportes

urlpatterns = [
    path('empresas/detail/<int:pk>', EmpresaDet.as_view(), name="empresa_det"),
    path('empresas/new',EmpresaNew.as_view(),name="empresa_new"),
    path('empresas/edit/<int:pk>', EmpresaEdit.as_view(), name="empresa_edit"),

    path('reportes/vista/compras', views.compras_list, name='compras_list'),
    path('reportes/vista/ventas', views.ventas_list, name='ventas_list'),
    path('reportes/vista/venta/detail/<int:factura_id>', views.venta_detail, name = 'venta_detail'),
    path('reportes/vista/alerta/catidad', views.alerta_cantidad, name='alerta_cantidad_list'),
    path('reportes/vista/proveedores', views.proveedores_list, name='proveedores_list'),
    path('reportes/vista/clientes', views.clientes_list, name='clientes_list'),
    path('reportes/vista/proveedor/history/<int:proveedor_id>', views.proveedor_history, name='proveedor_history'),
    path('reportes/vista/cliente/history/<int:cliente_id>', views.cliente_history, name='cliente_history'),
    path('reportes/vista/devolucion/compras', views.devolucion_compras_list, name='devolucion_compras_list'),
    path('reportes/vista/devolucion/facturas', views.devolucion_facturas_list, name='devolucion_facturas_list'),
    path('reportes/vista/almacen', views.almacen_list, name = 'almacen_list'),

    path('reportes/reporte/compras', reportes.compras_list, name='compras_list_report'),
    path('reportes/reporte/ventas', reportes.ventas_list, name='ventas_list_report'),
    path('reportes/reporte/factura/venta/<int:factura_id>', reportes.facura_venta, name='factura_venta'),
]
