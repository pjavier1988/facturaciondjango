from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Empresa
from .forms import EmpresaForm

class EmpresaView(LoginRequiredMixin, generic.ListView):

    model = Empresa
    template_name = "param/empresa_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

class EmpresaDet(LoginRequiredMixin, generic.DetailView):

    model = Empresa
    template_name = "param/empresa_det.html"
    context_object_name = "obj"
    login_url = "bases:login"

class EmpresaNew(LoginRequiredMixin, generic.CreateView):

    model = Empresa
    template_name = "param/empresa_form.html"
    context_object_name = "obj"
    form_class = EmpresaForm
    success_url = reverse_lazy("inv:marca_list")
    login_url = "bases:login" 
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)