from django.urls import path
from .views import EmpresaDet, EmpresaNew, EmpresaEdit

urlpatterns = [
    path('empresas/detail/<int:pk>', EmpresaDet.as_view(), name="empresa_det"),
    path('empresas/new',EmpresaNew.as_view(),name="empresa_new"),
    path('empresas/edit/<int:pk>', EmpresaEdit.as_view(), name="empresa_edit"),

]