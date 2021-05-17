from .forms import ProveedorForm
from .models import Proveedor
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProveedorView(LoginRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_proveedor"

class ProveedorNew(LoginRequiredMixin,
                   generic.CreateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo"
    permission_required="cmp.add_proveedor"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        #print(self.request.user.id)
        return super().form_valid(form)


class ProveedorEdit(LoginRequiredMixin,
                   generic.UpdateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Editado"
    permission_required="cmp.change_proveedor"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)

def proveedor_inactivar(request,id):
    template_name = "cmp/inactivar_prv.html"
    contexto = {}
    return render(request,template_name,contexto)