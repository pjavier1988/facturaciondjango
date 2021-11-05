from django.urls import path
from . import views

urlpatterns = [
    path('nomina/list/', views.nomina_list, name='nomina_list'),
    path('nomina/', views.nomina, name='nomina'),
    path('personas/', views.EmpleadoView.as_view(), name='personas'), #Main URL

    path('roles/new/',views.RolNew.as_view(), name="rol_new"),
    path('roles/edit/<int:pk>',views.RolEdit.as_view(), name="rol_edit"),
    path('roles/status/<int:id>',views.rol_inactivar, name="rol_inactivar"),

    path('empleados/new/',views.EmpleadoNew.as_view(), name="empleado_new"),
    path('empleados/edit/<int:pk>',views.EmpleadoEdit.as_view(), name="empleado_edit"),
    path('empleados/status/<int:id>',views.empleado_inactivar, name="empleado_inactivar"),

    path('empleado-hrex/new/',views.EmpleadoHoraExtraNew.as_view(), name="empleado_hrex_new"),
]