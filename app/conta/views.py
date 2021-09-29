from django.shortcuts import render

# Create your views here.

def nomina_list(request):

    template_name = 'conta/nomina_list.html'

    context = {
    }

    return render(request, template_name, context)