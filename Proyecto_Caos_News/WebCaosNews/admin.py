from django.contrib import admin
from .models import UserProfile,Categoria,Contacto,Galeria,Noticia

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Categoria)
admin.site.register(Noticia)
admin.site.register(Galeria)
admin.site.register(Contacto)
