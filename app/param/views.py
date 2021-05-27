from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Empresa, User
from .forms import EmpresaForm
from django.contrib import messages

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
    login_url = "bases:login"
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    #DOC
    #https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-simple/

    def get_success_url(self):
        if set_user_company(self.request.user.id, self.object) == False:
            messages.error(self.request,'Super Usuario solo puede tener una empresa')
        return reverse_lazy('param:empresa_det', kwargs={'pk': self.object.pk})

class EmpresaEdit(LoginRequiredMixin, generic.UpdateView):

    model = Empresa
    template_name = "param/empresa_form.html"
    context_object_name = "obj"
    form_class = EmpresaForm
    login_url = "bases:login"
    
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('param:empresa_det', kwargs={'pk': self.object.pk})

#Funciones

def set_user_company(user_id, company):

    user = User.objects.filter(pk=user_id).first()

    if user:
        if user.company == None:
            user.company = company
            user.save()
            return True
        else:
            return False