from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey
from django.conf import settings

# Create your models here.
class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    um = models.IntegerField(blank=True,null=True)

    #Para no migrar, pero si se puede heredar
    class Meta:
        abstract = True


class ClaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    # uc = models.ForeignKey(User, on_delete=models.CASCADE)
    # um = models.IntegerField(blank=True,null=True)
    uc = UserForeignKey(auto_user_add=True,related_name='+')
    um = UserForeignKey(auto_user=True,related_name='+')

    class Meta:
        abstract=True

class AUDUsers(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract = True