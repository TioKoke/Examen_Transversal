from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', Home,name='HOME'),
    path('BuscaNoticia/', BuscaNoticia,name='BUSCA'),
    path('Galeria/', Galeria1,name='GALE'),
    path('Registro/', Registro,name='REGIS'),
    path('AgregarNoticia/', AgregarNoticia,name='AGRE'),
    path('Login/', Login,name='LOGI'),
    path('Contacto/', Contactos,name='CONT'),
    path('Noticia0/<id>/', Noticia0,name='NOTI'),
    path('Cerrar/', cerrar_sesion,name='CERRAR'),
    path('eliminar/<id>/',eliminar,name='ELI'),
    path('modificar/<id>/',modificar,name='MOD'),
    path('modificar/',modificarNoticia,name='MODN'),
    path('insertar/',insertar,name='INSERT'),
    path('ficha_buscar/',ficha_buscar,name='BUSCARF'),
    path('buscar_cate/<id>/',buscar_tipo,name='BUSCART'),
    path('Perfil/', Perfil,name='PERFIL'),
    path('Periodistas/', Periodistas,name='PERI'),
    path('EditarPerfil/', Editar_Per,name='EDIPER'),
]
