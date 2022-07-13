import email
import random
import string
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
#Llamamos el model base de usuario para crear nuestro user
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, first_name, last_name, password, **other_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Correo'), unique= True)
    first_name = models.CharField(max_length=100,default='--')
    last_name = models.CharField(max_length=100,default='--')
    profile_pic = models.ImageField(upload_to='users', default ='User_Defecto.jpg')
    bio = models.TextField(_('Biografia'), max_length=500,blank=True)
    register_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Categoria(models.Model):
    nombre = models.CharField(primary_key=True,max_length=20)
    imagen = models.ImageField(upload_to='fotos',default='Falta_imagen.jpg')
    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    id_not = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=300,default='--')
    subtitulo = models.CharField(max_length=300,default='--')
    historia = models.CharField(max_length=10000,default='--')
    ubicacion = models.CharField(max_length=80,default='--')
    imagen = models.ImageField(upload_to='fotos',default='Falta_imagen.jpg')
    publicar = models.BooleanField(default=False)
    comentario = models.TextField(default='--')
    register_date = models.DateTimeField(default=timezone.now)
    nombre = models.ForeignKey(Categoria,on_delete=models.CASCADE,default='--')
    usuario = models.CharField(max_length=60,default='--')
    nombre_usu = models.CharField(max_length=100,default='--')

    def __str__(self):
        return 'Numero:'+str(self.id_not)

class Galeria(models.Model):
    auto_inc = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='galeria')
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    def __str__(self):
        return 'Numero:'+str(self.auto_inc)

class Contacto(models.Model):
    contador = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=300,default='--')
    nombre = models.CharField(max_length=300,default='--')
    correo = models.CharField(max_length=300,default='--')
    telefono = models.CharField(max_length=300,default='--')
    region = models.CharField(max_length=300,default='--')
    ciudad = models.CharField(max_length=300,default='--')
    termino = models.BooleanField(default=False)
    def __str__(self):
        return 'Numero:'+str(self.contador)