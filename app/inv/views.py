from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Categoria, Producto,SubCategoria,Marca,UnidadMedida, Perdidas
from .forms import CategoriaForm, ProductoForm,SubCategoriaForm,MarcaForm,UnidadMedidaForm

#Categorias ************************************************************************************************************************************

class CategoriaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):

    permission_required= "inv.view.categoria"
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):

        if self.request.user.company:
            return Categoria.objects.filter(empresa = self.request.user.company)
        else:
            return None

class CategoriaNew(SuccessMessageMixin, LoginRequiredMixin,generic.CreateView):

    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"
    success_message = "Categoría creada exitosamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)

class CategoriaEdit(SuccessMessageMixin, LoginRequiredMixin,generic.UpdateView):

    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"
    success_message = "Categoría editada existosamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class CategoriaDelete(LoginRequiredMixin,generic.DeleteView):

    model = Categoria
    template_name = "inv/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:producto_list")

# Sub Categoria ********************************************************************************************************************************

class SubCategoriaView(LoginRequiredMixin, generic.ListView):

    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):

        if self.request.user.company:
            return SubCategoria.objects.filter(empresa = self.request.user.company)
        else:
            return None

class SubCategoriaNew(LoginRequiredMixin,generic.CreateView):

    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    #http://django-vanilla-views.org/api/base-views
    def get_form(self, form_class=None):
        return SubCategoriaForm(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)

class SubCategoriaEdit(LoginRequiredMixin,generic.UpdateView):

    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

    #https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class
    def get_form(self, form_class=None):
        return SubCategoriaForm(self.request.user, **self.get_form_kwargs())

class SubCategoriaDelete(LoginRequiredMixin,generic.DeleteView):

    model = SubCategoria
    template_name = "inv/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:producto_list")

#Marca *****************************************************************************************************************************************

class MarcaView(LoginRequiredMixin, generic.ListView):

    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):

        if self.request.user.company:
            return Marca.objects.filter(empresa = self.request.user.company)
        else:
            return None


class MarcaNew(LoginRequiredMixin,generic.CreateView):

    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)


class MarcaEdit(LoginRequiredMixin,generic.UpdateView):

    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def marca_inactivar(request,id):

    marca = Marca.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/catalogos_del.html"

    if not marca:
        redirect("inv:marca_list")

    if request.method == 'GET':
        contexto = {"obj":marca}

    if request.method == 'POST':
        marca.estado = False
        marca.save()
        messages.success(request, 'Marca Inactivado')
        return HttpResponseRedirect(reverse('inv:producto_list'))
        #redirect("inv/marca_list")

    return render(request,template_name,contexto)

#Unidades de Medida ****************************************************************************************************************************

class UnidadMedidaView(LoginRequiredMixin, generic.ListView):

    model = UnidadMedida
    template_name = "inv/unidadmedida_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):

        if self.request.user.company:
            return UnidadMedida.objects.filter(empresa = self.request.user.company)
        else:
            return None


class UnidadMedidaNew(LoginRequiredMixin,generic.CreateView):

    model = UnidadMedida
    template_name = "inv/unidadmedida_form.html"
    context_object_name = "obj"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)


class UnidadMedidaEdit(LoginRequiredMixin,generic.UpdateView):

    model = UnidadMedida
    template_name = "inv/unidadmedida_form.html"
    context_object_name = "obj"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def unidadmedida_inactivar(request,id):

    unidad = UnidadMedida.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/catalogos_del.html"
    if not unidad:
        return HttpResponseRedirect(reverse('inv:producto_list'))

    if request.method == 'GET':
        contexto = {"obj":unidad}

    if request.method == 'POST':
        unidad.estado = False
        unidad.save()

        return HttpResponseRedirect(reverse('inv:producto_list'))
        #redirect("inv/marca_list")

    return render(request,template_name,contexto)

#Productos ***************************************************************************************************************************************

class ProductoView(LoginRequiredMixin, generic.ListView):

    model = Producto
    template_name = "inv/producto_list.html"
    context_object_name = "productos"
    login_url = "bases:login"

    def get_queryset(self):

        if self.request.user.company:
            return Producto.objects.filter(empresa = self.request.user.company)
        else:
            return None

    def get_context_data(self, **kwargs):

        context = super(ProductoView, self).get_context_data(**kwargs) # get the default context data
        context['categorias'] = Categoria.objects.filter( # add extra field to the context
            empresa=self.request.user.company,
        )
        context['sub_categorias'] = SubCategoria.objects.filter( # add extra field to the context
            empresa=self.request.user.company,
        )
        context['marcas'] = Marca.objects.filter( # add extra field to the context
            empresa=self.request.user.company,
        )
        context['unidades_medida'] = UnidadMedida.objects.filter( # add extra field to the context
            empresa=self.request.user.company,
        )

        return context

class ProductoNew(LoginRequiredMixin, generic.CreateView):

    model = Producto
    template_name = "inv/producto_form.html"
    context_object_name = 'obj'
    success_url = reverse_lazy("inv:producto_list")

    def get_form(self, form_class=None):
        return ProductoForm(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.uc = self.request.user
        form.instance.empresa = self.request.user.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(ProductoNew, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.filter(empresa=self.request.user.company)
        context["subcategorias"] = SubCategoria.objects.filter(empresa=self.request.user.company)
        return context

class ProductoEdit(LoginRequiredMixin,generic.UpdateView):

    model = Producto
    template_name = "inv/producto_form.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:producto_list")
    login_url = "bases:login"

    def get_form(self, form_class=None):
        return ProductoForm(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


def producto_inactivar(request,id):

    producto = Producto.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/catalogos_del.html"
    if not producto:
        return HttpResponseRedirect(reverse('inv:producto_list'))

    if request.method == 'GET':
        contexto = {"obj":producto}

    if request.method == 'POST':
        producto.estado = False
        producto.save()

        return HttpResponseRedirect(reverse('inv:producto_list'))
        #redirect("inv/marca_list")

    return render(request,template_name,contexto)
def perdidas(request):
    template_name='inv/perdidas.html'
    perdida = Perdidas.objects.all()

    context ={
        'obj':perdida,
    }
    return render(request, template_name, context)
