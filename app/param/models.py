from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from bases.models import AUDUsers, ClaseModelo
from django.core.files.base import ContentFile

class Empresa(ClaseModelo):

    COL = 'Colombia'
    ECU = 'Ecuador'

    PAISES = [
        (COL, 'Colombia'),
        (ECU, 'Ecuador'),
    ]

    nombre = models.CharField(max_length=20, null=False, blank=False)
    nombre_completo = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=15, null=False, blank=False)
    direccion = models.CharField(max_length=200, null=False, blank=False)
    correo = models.CharField(max_length=320, null=False, blank=False)
    logo = models.FileField(upload_to='img/empresa', null=True)
    ruc = models.CharField(max_length=100, null=True)
    tributa = models.BooleanField(default=True, null=False)
    pais = models.CharField(max_length=20, null=False, choices=PAISES, default=COL)

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name_plural = "Empresas"

class Links(ClaseModelo):

    FACEBOOK = 'Facebook'
    CAROUSEL = 'Carousel'
    YOUTUBE = 'YouTube'
    TWITTER = 'Twitter'
    INSTAGRAM = 'Instagram'
    LINKEDIN = 'LinkedIn'

    PLATAFORMAS = [
        (FACEBOOK, 'Facebook'),
        (CAROUSEL, 'Carousel'),
        (YOUTUBE, 'YouTube'),
        (TWITTER, 'Twitter'),
        (INSTAGRAM, 'Instagram'),
        (LINKEDIN, 'LinkedIn'),
    ]

    plataforma = models.CharField(max_length=20, null=False, choices=PLATAFORMAS, default=CAROUSEL)
    url = models.CharField(max_length=400, null=True)
    imagen = models.FileField(upload_to='img/carousel', null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False)

class UserManager(BaseUserManager):
    def _create_user(self, username, email, name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, name,last_name, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, AUDUsers):

    username = models.CharField(max_length = 255, unique = True)
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    image = models.CharField('Imagen de perfil', max_length=255, null=True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    company = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name','last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'
