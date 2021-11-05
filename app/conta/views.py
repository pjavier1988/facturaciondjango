from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from bases.views import SinPrivilegios
from fac.models import Cliente
from cmp.models import Proveedor
from .models import Rol, Empleado, HoraExtra, EmpleadoHoraExtra
from .forms import RolForm, EmpleadoForm, EmpleadoHoraExtraForm, HoraExtraForm

MAIN_VIEW = 'conta:personas'
EMPLEADO_FORM_TEMPLATE = 'conta/empleado_form.html'
ROL_FORM_TEMPLATE = 'conta/rol_form.html'
HORA_EXTRA_TEMPLATE = 'conta/hora_extra_form.html'
EMPLEADO_HREX_FORM_TEMPLATE = 'conta/empleado_hrex_form.html'
NOMINA_TEMPLATE = 'conta/nomina.html'

class VistaBaseCreate(SuccessMessageMixin, SinPrivilegios, generic.CreateView):

    context_object_name = 'obj'
    success_message="Registro Agregado"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):

    context_object_name = 'obj'
    success_message="Registro Actualizado"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

#Empleado **********************************************************************************************************************

class EmpleadoView(LoginRequiredMixin, generic.ListView):

    model = Empleado
    template_name = "conta/personas.html"
    context_object_name = "empleados"
    login_url = "bases:login"

    def get_queryset(self):

        if self.request.user.company:
            return Empleado.objects.filter(empresa = self.request.user.company)
        else:
            return None

    def get_context_data(self, **kwargs):

        context = super(EmpleadoView, self).get_context_data(**kwargs) # get the default context data

        context['proveedores'] = Proveedor.objects.filter( # add extra field to the context
            empresa=self.request.user.company,
        )
        context['clientes'] = Cliente.objects.filter(
            empresa=self.request.user.company,
        )
        context['roles'] = Rol.objects.filter(
            empresa=self.request.user.company,
        )

        return context

class EmpleadoNew(VistaBaseCreate):

    model = Empleado
    template_name = EMPLEADO_FORM_TEMPLATE
    success_url = reverse_lazy(MAIN_VIEW)
    permission_required = "conta.add_empleado"

    def get_form(self, form_class=None):
        return EmpleadoForm(self.request.user, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        form = EmpleadoForm(self.request.user, **self.get_form_kwargs())
        return render(request, self.template_name, {'form': form})


class EmpleadoEdit(VistaBaseEdit):

    model = Empleado
    template_name = EMPLEADO_FORM_TEMPLATE
    form_class = EmpleadoForm
    success_url = reverse_lazy(MAIN_VIEW)
    permission_required = "conta.change_rol"

    def get_form(self, form_class=None):
        return EmpleadoForm(self.request.user, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)

        return self.render_to_response(context)

@login_required(login_url="/login/")
@permission_required("fac.change_empleado", login_url="/login/")
def empleado_inactivar(request, id):

    empleado = Empleado.objects.filter(pk=id, empresa=request.user.company).first()

    if request.method=="POST":

        if empleado:

            empleado.estado = not empleado.estado
            empleado.save()
            return HttpResponse("OK")

        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

#Rol *******************************************************************************************************************************

class RolNew(VistaBaseCreate):

    model = Rol
    template_name = ROL_FORM_TEMPLATE
    form_class = RolForm
    success_url = reverse_lazy(MAIN_VIEW)
    permission_required = "conta.add_rol"

    def get(self, request, *args, **kwargs):
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

class RolEdit(VistaBaseEdit):

    model = Rol
    template_name = ROL_FORM_TEMPLATE
    form_class = RolForm
    success_url = reverse_lazy(MAIN_VIEW)
    permission_required = "conta.change_rol"

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)

        return self.render_to_response(context)

@login_required(login_url="/login/")
@permission_required("fac.change_rol", login_url="/login/")
def rol_inactivar(request, id):

    rol = Rol.objects.filter(pk=id, empresa=request.user.company).first()

    if request.method=="POST":

        if rol:

            rol.estado = not rol.estado
            rol.save()
            return HttpResponse("OK")

        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

#Empleados - Hora Extra ************************************************************************************************************

class EmpleadoHoraExtraNew(VistaBaseCreate):

    model = EmpleadoHoraExtra
    template_name = EMPLEADO_HREX_FORM_TEMPLATE
    success_url = reverse_lazy(NOMINA_TEMPLATE)
    permission_required = "conta.add_empleadohoraextra"

    def get_form(self, form_class=None):
        return EmpleadoHoraExtraForm(self.request.user, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        form = EmpleadoHoraExtraForm(self.request.user, **self.get_form_kwargs())
        return render(request, self.template_name, {'form': form})

#Nómina ***************************************************************************************************************************

def nomina_list(request):

    template_name = 'conta/nomina_list.html'

    context = {
    }

    return render(request, template_name, context)

def nomina(request):

    template_name = NOMINA_TEMPLATE

    empleados = Empleado.objects.filter(empresa=request.user.company)
    empleados_hrex = EmpleadoHoraExtra.objects.filter(empresa=request.user.company)

    context = {
        'empleados': empleados,
        'empleados_hrex': empleados_hrex,
    }

    return render(request, template_name, context)