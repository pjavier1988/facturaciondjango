from django.contrib import admin
from .models import User, Empresa

admin.site.register([User, Empresa])