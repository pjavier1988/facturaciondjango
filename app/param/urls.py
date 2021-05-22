from django.urls import path
from .views import EmpresaDet, EmpresaNew

urlpatterns = [
    path('empresas/detail/<int:pk>', EmpresaDet.as_view(), name="empresa_det"),
    path('empresas/new',EmpresaNew.as_view(),name="empresa_new"),
]