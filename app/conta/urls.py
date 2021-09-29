from django.urls import path
from . import views

urlpatterns = [
    path('nomina/list/', views.nomina_list, name='nomina_list'),
]