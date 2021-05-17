from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Categoria, Producto,SubCategoria,Marca,UnidadMedida
from .forms import CategoriaForm, ProductoForm,SubCategoriaForm,MarcaForm,UnidadMedidaForm
# Create your views here.

class CategoriaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required= "inv.view.categoria"
    model = Categoria
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login"   

class CategoriaNew(SuccessMessageMixin, LoginRequiredMixin,generic.CreateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categoria_list")
    login_url = "bases:login" 
    success_message = "Categoría creada exitosamente"
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class CategoriaEdit(SuccessMessageMixin, LoginRequiredMixin,generic.UpdateView):
    model = Categoria
    template_name = "inv/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inv:categoria_list")
    login_url = "bases:login" 
    success_message = "Categoría editada existosamente"
    
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class CategoriaDelete(LoginRequiredMixin,generic.DeleteView):
    model = Categoria
    template_name = "inv/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:categoria_list")

'''TODAS LAS VISTAS DE SUBCATEGORIA'''
class SubCategoriaView(LoginRequiredMixin, generic.ListView):
    model = SubCategoria
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"
    login_url = "bases:login" 

class SubCategoriaNew(LoginRequiredMixin,generic.CreateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategoria_list")
    login_url = "bases:login" 
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class SubCategoriaEdit(LoginRequiredMixin,generic.UpdateView):
    model = SubCategoria
    template_name = "inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inv:subcategoria_list")
    login_url = "bases:login" 
    
    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class SubCategoriaDelete(LoginRequiredMixin,generic.DeleteView):
    model = SubCategoria
    template_name = "inv/catalogos_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("inv:subcategoria_list")

'''TODAS LAS VISTAS DE MARCA'''
class MarcaView(LoginRequiredMixin, generic.ListView):
    model = Marca
    template_name = "inv/marca_list.html"
    context_object_name = "obj"
    login_url = "bases:login" 


class MarcaNew(LoginRequiredMixin,generic.CreateView):
    model = Marca
    template_name = "inv/marca_form.html"
    context_object_name = "obj"
    form_class = MarcaForm
    success_url = reverse_lazy("inv:marca_list")
    login_url = "bases:login" 
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    
class MarcaEdit(LoginRequiredMixin,generic.UpdateView):
        model = Marca
        template_name = "inv/marca_form.html"
        context_object_name = "obj"
        form_class = MarcaForm
        success_url = reverse_lazy("inv:marca_list")
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
        print("lleg'ue por aca")
        return HttpResponseRedirect(reverse('inv:marca_list'))
        #redirect("inv/marca_list")

    return render(request,template_name,contexto)



'''TODAS LAS VISTAS DE UNIDADES DE MEDIDA'''
class UnidadMedidaView(LoginRequiredMixin, generic.ListView):
    model = UnidadMedida
    template_name = "inv/unidadmedida_list.html"
    context_object_name = "obj"
    login_url = "bases:login" 


class UnidadMedidaNew(LoginRequiredMixin,generic.CreateView):
    model = UnidadMedida
    template_name = "inv/unidadmedida_form.html"
    context_object_name = "obj"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy("inv:unidadmedida_list")
    login_url = "bases:login" 
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    
class UnidadMedidaEdit(LoginRequiredMixin,generic.UpdateView):
        model = UnidadMedida
        template_name = "inv/unidadmedida_form.html"
        context_object_name = "obj"
        form_class = UnidadMedidaForm
        success_url = reverse_lazy("inv:unidadmedida_list")
        login_url = "bases:login" 
        
        def form_valid(self, form):
            form.instance.um = self.request.user.id
            return super().form_valid(form)


def unidadmedida_inactivar(request,id):
    unidad = UnidadMedida.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inv/catalogos_del.html"
    if not unidad:
        return HttpResponseRedirect(reverse('inv:unidadmedida_list'))

    if request.method == 'GET':
        contexto = {"obj":unidad}

    if request.method == 'POST':
        unidad.estado = False
        unidad.save()
        
        return HttpResponseRedirect(reverse('inv:unidadmedida_list'))
        #redirect("inv/marca_list")

    return render(request,template_name,contexto)



'''TODAS LAS VISTAS DE PRODUCTO'''
class ProductoView(LoginRequiredMixin, generic.ListView):
    model = Producto
    template_name = "inv/producto_list.html"
    context_object_name = "obj"
    login_url = "bases:login" 


class ProductoNew(LoginRequiredMixin,
                   generic.CreateView):
    model=Producto
    template_name="inv/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inv:producto_list")
    
    

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ProductoNew, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        return context
    
    
class ProductoEdit(LoginRequiredMixin,generic.UpdateView):
        model = Producto
        template_name = "inv/producto_form.html"
        context_object_name = "obj"
        form_class = ProductoForm
        success_url = reverse_lazy("inv:producto_list")
        login_url = "bases:login" 
        
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