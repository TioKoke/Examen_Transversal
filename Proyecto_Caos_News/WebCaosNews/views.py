from email.headerregistry import Group
from django.shortcuts import render
#importar modelo de socio
from .models import *
from django.contrib.auth.models import Group
#importar librerias que validan el ingreso o login
from django.contrib.auth import authenticate,logout,login as login_aut
# Create your views here.
from django.contrib.auth.decorators import login_required,permission_required

import requests
API_KEY= 'ee8732814db546feadf663f6271e6867'

def ultimas():
    noticias_ultimas = Noticia.objects.filter(publicar=True)[:3]
    return noticias_ultimas

def eliminar(request,id):
    usu = request.user.email
    notc = Noticia.objects.get(titulo=id)
    categorias = Categoria.objects.all()
    datos = UserProfile.objects.get(email = usu)
    notc.delete()
    mensaje="mascota eliminada"
    noticias = Noticia.objects.filter(usuario=request.user.email)
    cantidad = Noticia.objects.filter(usuario=request.user.email).count()
    contexto={"cantidad":cantidad,"noticias":noticias,"mensaje":mensaje, "items":categorias,"datos":datos}
    return render(request,"Perfil.html",contexto)

def cantidad_no_publicada(usu):
    print(usu)
    cant = Noticia.objects.filter(usuario=usu).filter(publicar=False).count()
    return cant

def Home(request):
    noticia_ultimas = Noticia.objects.filter(publicar=True)[:3]
    categoria = Categoria.objects.all()
    contexto ={"noticia_ultimas":noticia_ultimas,"categoria":categoria}
    return render(request,"Home.html",contexto)

def Galeria1(request):
    noticia_ultimas = Noticia.objects.filter(publicar=True)
    contexto ={"noticia_ultimas":noticia_ultimas}
    return render(request,"Galeria.html",contexto)

def Registro(request):
    contexto = {"msg":""}
    if request.POST:
        c = request.POST.get("txtCorreo")
        n = request.POST.get("txtNombre")
        l = request.POST.get("txtApellido")
        p = request.POST.get("txtContra")
        g = Group.objects.get(name='Periodista')
        user = UserProfile()
        user.email = c
        user.first_name = n 
        user.last_name = l
        user.is_active = True 
        user.set_password(p)
        user.save()
        g.user_set.add(user)
        #cm= CustomAccountManager()
        #cm.create_user(email = c,first_name = n, last_name = l, password =p)
        contexto = {"msg":"Guardado"}
        return render(request,"Login.html",contexto)
    return render(request,"Registro.html",contexto)

def cerrar_sesion(request):
    logout(request)
    contexto={"noticia_ultimas":ultimas()}
    return render(request,"Home.html",contexto)

def Login(request):
    contexto={"msg":""}
    if request.POST:
        usuario = request.POST.get("txtCorreo")
        contra = request.POST.get("txtContra")
        print(usuario)
        print(contra)
        us = authenticate(request,email=usuario,password=contra)
        if us is not None and us.is_active:
            login_aut(request,us)
            c= cantidad_no_publicada(request.user.email)            
            contexto={"cantidad":c,"noticia_ultimas":ultimas()}
            return render(request,'Home.html',contexto)
        else:
            contexto={"msg":"Usuario o contraseña incorrecto"}
    return render(request,"Login.html",contexto)

def Contactos(request):
    if request.POST:
        r = request.POST.get("txtRut")
        n = request.POST.get("txtNombre")
        c = request.POST.get("txtCorreo")
        t = request.POST.get("txtFono")
        re = request.POST.get("txtRegion")
        ci = request.POST.get("txtCiudad")
        te = True
        con = Contacto()
        con.rut = r
        con.nombre = n
        con.correo = c
        con.telefono = t
        con.region = re
        con.ciudad = ci
        con.termino = te
        con.save()
    return render(request,"Contacto.html")

def Cultural(request):    
    noticia_ultimas = Noticia.objects.filter(publicar=True).filter(nombre="Cultural")
    contexto ={"noticia_ultimas":noticia_ultimas}
    return render(request,"Cultural.html",contexto)

def Nacional(request):
    noticia_ultimas = Noticia.objects.filter(publicar=True).filter(nombre="Regional")
    contexto ={"noticia_ultimas":noticia_ultimas}
    return render(request,"Nacional.html",contexto)

def Regional(request):
    noticia_ultimas = Noticia.objects.filter(publicar=True).filter(nombre="Nacional")
    contexto ={"noticia_ultimas":noticia_ultimas}
    return render(request,"Regional.html",contexto)

def Educacional(request):
    noticia_ultimas = Noticia.objects.filter(publicar=True).filter(nombre="Educacional")
    contexto ={"noticia_ultimas":noticia_ultimas}
    return render(request,"Educacional.html",contexto)

def BuscaNoticia(request):
    Query = request.POST.get("Query")
    if Query:
        url =f'https://newsapi.org/v2/everything?q={Query}&language=es&sortby=popularity&apikey={API_KEY}'
        response = requests.get(url)
        data=response.json()
        articles = data['articles']

    else:
        Query="1hola"
        url =f'https://newsapi.org/v2/everything?q={Query}&language=es&sortby=popularity&apikey={API_KEY}'
        response = requests.get(url)
        data=response.json()
        articles = data['articles']

    context = {
        'articles' : articles,
    }
    return render(request,"BuscaNoticia.html",context)

@login_required(login_url='/Login/')
@permission_required('WebCaosNews.add_galeria',login_url='/Login/')
@permission_required('WebCaosNews.view_galeria',login_url='/Login/')
@permission_required('WebCaosNews.add_noticia',login_url='/Login/')
@permission_required('WebCaosNews.view_noticia',login_url='/Login/')
@permission_required('WebCaosNews.delete_noticia',login_url='/Login/')
@permission_required('WebCaosNews.change_noticia',login_url='/Login/')
def AgregarNoticia(request):
    usu = request.user.email
    nam_usu = request.user.first_name
    las_usu = request.user.last_name
    nom_compe = f"{nam_usu} {las_usu}" 
    categorias = Categoria.objects.all() 
    noticias = Noticia.objects.filter(usuario = usu)
    cantidad = Noticia.objects.filter(usuario= usu).count()
    contexto={"items":categorias,"noticias":noticias,"cantidad":cantidad}
    if request.POST:
        titulo = request.POST.get("txtTitular")
        subtitulo = request.POST.get("txtSubtitulo")
        historia = request.POST.get("txtEscribir")
        ubicacion = request.POST.get("txtUbicacion")
        imagen = request.FILES.get("txtImagen")
        catego = request.POST.get("cboCategoria")
        # seleccionar el registro completo de la categoria a buscar
        obj_catego = Categoria.objects.get(nombre=catego)
        mensaje=""
        try:
            mas = Noticia()
            mas.titulo = titulo
            mas.subtitulo = subtitulo
            mas.historia = historia
            mas.ubicacion = ubicacion
            if imagen is not None:
                mas.imagen = imagen
            mas.nombre = obj_catego
            mas.usuario = usu
            mas.nombre_usu = nom_compe
            mas.save()
            mensaje ="Grabo Noticia"
        except:
            mensaje ="No Grabo Noticia"
        contexto["mensaje"]=mensaje

    return render(request,"AgregarNoticia.html",contexto)

def modificar(request,id):
    noticia = Noticia.objects.get(titulo=id)
    categorias = Categoria.objects.all()
    contexto={"noticias":noticia, "items":categorias}
    return render(request,"AgregarNoticiaMod.html",contexto)

@login_required(login_url='/Login/')
def modificarNoticia(request):
    usu = request.user.email
    categorias = Categoria.objects.all()
    noticias = Noticia.objects.filter(usuario= usu) 
    cantidad = Noticia.objects.filter(usuario= usu).count()
    contexto={"items":categorias,"noticias":noticias,"cantidad":cantidad}
    if request.POST:
        id = request.POST.get("txtID")
        titulo = request.POST.get("txtTitular")
        subtitulo = request.POST.get("txtSubtitulo")
        historia = request.POST.get("txtEscribir")
        ubicacion = request.POST.get("txtUbicacion")
        imagen = request.FILES.get("txtImagen")
        catego = request.POST.get("cboCategoria")
        # seleccionar el registro completo de la categoria a buscar
        obj_catego = Categoria.objects.get(nombre=catego)
        mensaje=""
        try:
            mas = Noticia.objects.get(id_not=id)
            mas.titulo = titulo
            mas.subtitulo = subtitulo
            mas.historia = historia
            mas.ubicacion = ubicacion
            if imagen is not None:
                mas.imagen = imagen
            mas.nombre = obj_catego
            mas.usuario = usu
            mas.save()
            mensaje ="Modifico noticia"
        except:
            mensaje ="No Modifico Noticia"
        contexto["mensaje"]=mensaje
    return render(request,"AgregarNoticiaMod.html",contexto)

def insertar(request):
    mensaje = ""
    if request.POST:
        noticia = Noticia.objects.get(id_not = request.POST.get("txtIdnot"))
        imagen = request.FILES.get("txtImagen")
        gale = Galeria()
        gale.imagen = imagen
        gale.noticia = noticia
        gale.save()
        mensaje = "Imagen de la noticia "
    usu = request.user.email
    datos = UserProfile.objects.get(email = usu)
    categorias = Categoria.objects.all() 
    noticias = Noticia.objects.filter(usuario= usu) 
    cantidad = Noticia.objects.filter(usuario= usu).count()
    contexto={"items":categorias,"noticias":noticias,"cantidad":cantidad,"mensaje":mensaje,"datos":datos}

    return render(request,"Perfil.html",contexto)

def Galeria2(request,id):
    noticia_obj = Noticia.objects.get(titulo=id)
    usuario_obj = Noticia.objects.get(usuario=id)
    galeria = Galeria.objects.filter(noticia=noticia_obj)
    contexto={"noticia":noticia_obj,"galeria":galeria,"usuario":usuario_obj}
    return render(request,"galeria2.html",contexto)

def Noticia0(request,id):
    noticia_obj = Noticia.objects.filter(id_not=id)
    galeria = Galeria.objects.filter(noticia=id)
    contexto={"noticia_obj":noticia_obj,"galeria":galeria }
    return render(request,"noticia0.html",contexto)

def ficha_buscar(request):
    contexto={"mensaje":"Noticia no encontrada"}
    if request.POST:
        try:
            noticia_obj = Noticia.objects.filter(titulo = request.POST.get("txtBuscar"))
            usuario_obj = Noticia.objects.filter(usuario = request.POST.get("txtBuscar"))
            contexto={"noticia":noticia_obj,"mensaje":"Noticia encontrada","usuario":usuario_obj}
        except:
            contexto={"mensaje":"Noticia no encontrada"}
    return render(request,"galeria2.html",contexto)

def buscar_tipo(request,id):
    cate_obj = Categoria.objects.get(nombre=id)
    noticias = Noticia.objects.filter(nombre= cate_obj).filter(publicar=True)
    contexto={"noticia":noticias}

    return render(request,"galeria2.html",contexto)

@login_required(login_url='/Login/')
def Perfil(request):
    usu = request.user.email
    datos = UserProfile.objects.get(email = usu)
    categorias = Categoria.objects.all() 
    noticias = Noticia.objects.filter(usuario = usu)
    cantidad = Noticia.objects.filter(usuario= usu).count()
    contexto={"items":categorias,"noticias":noticias,"cantidad":cantidad,"datos":datos}
    return render(request,"Perfil.html",contexto)

@login_required(login_url='/Login/')
def Editar_Per(request):
    usu = request.user.email
    datos = UserProfile.objects.get(email = usu)
    categorias = Categoria.objects.all() 
    noticias = Noticia.objects.filter(usuario = usu) 
    cantidad = Noticia.objects.filter(usuario= usu).count()
    contexto={"items":categorias,"noticias":noticias,"cantidad":cantidad,"datos":datos}
    if request.POST:
        correo = request.POST.get("txtCorreo")
        first = request.POST.get("txtNombre")
        last = request.POST.get("txtApellido")
        biografia = request.POST.get("txtBio")
        imagen = request.FILES.get("txtImagen")
        mensaje = " "
        try:
            profile = UserProfile.objects.get(email = correo)
            profile.first_name = first
            profile.last_name = last
            profile.bio = biografia
            if imagen is not None:
                profile.profile_pic = imagen
            profile.save()
            mensaje = "Perfil Modificado"
        except:
            mensaje = "Perfil No Modificado"
        contexto["mensaje"]=mensaje     
    return render(request,"Editar_Perfil.html",contexto)

def Periodistas(request):
    perio_api = requests.get("http://127.0.0.1:8000/api/periodistas/").json()
    contexto = {"periodistas":perio_api,"noticia_ultimas":ultimas()}
    return render(request,"Periodistas.html",contexto)