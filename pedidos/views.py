from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import   login_required
import random
from materiales.models import Materiales
from django.db.models import Q
from utils.paginador import paginador_general
from usuarios.models import Usuario
from  utils.paginador import paginador_general
from django.urls import reverse
from datetime import datetime
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from datetime import datetime

from .utils.enviar_notificacion import enviar_notificacion_pedido

from .models import Pedido, Autorizacion_pedido

from logs.views import crear_log_sistema
@login_required
def index(request):
    fecha_actual = datetime.now()
    gestion = fecha_actual.year
    pagina_actual = request.GET.get('limit', 10)
    pedido_pendiente= lista_pedidos_por_estado(request,'pendiente')
    nombre_categoria='materiales'
    if (request.method == 'POST'):
        id_categoria = request.POST.get('categoria_id')
        if not id_categoria:
            return redirect('index')
        productos_categoria= Materiales.objects.select_related('categoria').filter(categoria_id=id_categoria, es_habilitado=True, gestion=gestion,  stock__gte = 1)
        productos_categoria= paginador_general(request,productos_categoria, pagina_actual)
        if productos_categoria and productos_categoria[0].categoria.nombre:
            nombre_categoria = productos_categoria[0].categoria.nombre
        else:
            nombre_categoria = 'materiales'


    else:
        productos_categoria= Materiales.objects.select_related('categoria').filter(es_habilitado=True, gestion=gestion, stock__gte = 1)
        productos_categoria= paginador_general(request, productos_categoria, pagina_actual)
       

    context ={
            'data1':pedido_pendiente,
            'data':productos_categoria,
            'categoria':nombre_categoria
         
                }
    return render(request, 'pedidos/index.html', context)
   


@login_required
def buscador(request):
    limit = request.GET.get('limit', 10)
    nombre_categoria = 'materiales'
    data_buscador = request.GET.get('buscador','')
    producto  = Materiales.objects.select_related('categoria').filter(Q(nombre__icontains=data_buscador) | Q(codigo__icontains=data_buscador) |  Q(marca__icontains=data_buscador), es_habilitado= True)
    producto = paginador_general(request, producto, limit)
    context={
        'data':producto,
        'categoria':nombre_categoria
    }
    return  render(request, 'pedidos/index.html', context)

def listar_info_material(request,id_material):
  
    material =  get_object_or_404(Materiales, pk=id_material)
    data={
        'id':material.id,
        'codigo':material.codigo,
        'nombre':material.nombre
    }   
    return JsonResponse({"data":data})
#------------------------------

@login_required
def realizar_pedido(request):
    id_usuario= request.user.id
    if request.method =='POST':
       try:
            id_material=request.POST["id_material"]
            cantidad_pedido =request.POST["cantidad_pedido"]
            if not id_material or not cantidad_pedido:
                 return JsonResponse({"error":"Los campos son obligatorios"})
            usuario = get_object_or_404(Usuario, id=id_usuario)
            material = get_object_or_404(Materiales, id=id_material)
            if int(cantidad_pedido) <=  0:
                return JsonResponse({"error":"Ingrese un numero mayor a 0", })
            if int(cantidad_pedido) > material.stock:
                return JsonResponse({"error":f"Solo queda: {material.stock} en el material: {material.nombre}",})
            total =  material.stock- int(cantidad_pedido)
            pedido= Pedido.objects.create(
                                          cantidad_pedida=int(cantidad_pedido),
                                          usuario=usuario,
                                          material=material)
      
            material.stock= total
            pedido.save()
            material.save()
            detalle = f'El usuario {request.user.username} ha seleccionado un pedido con el ID {pedido.id}.'
            crear_log_sistema(request.user.username, 'Seleccionar pedido', detalle, 'Pedidos')
            return JsonResponse({"data":"Pedido Realizado"})
       except Exception as e:
           print("ERROR", e)
           return JsonResponse({"error":"Ocurrio un error al realiza el pedido"})
           
def generar_numero_unico():
    pedidos = Pedido.objects.count()
    return pedidos
@login_required
def cambiar_estado_pedido(request):
    id_usuario= request.user.id
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    if usuario.cargo == 'Encargado_unidad':
        if request.method == 'GET':
            ids = request.GET.getlist('id')
            numero = generar_numero_unico()
            for id in ids:
                pedido= get_object_or_404(Pedido, pk=id)
                pedido.estado_de_pedido='realizado'
                pedido.numero_pedido=numero
                pedido.aprobado_oficina= True
                pedido.aprobado_unidad = True
                pedido.save()
                autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
                autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
                autorizacion_pedido.save()
                enviar_notificacion_pedido(pedido)
                detalle = f'El usuario {request.user.username} ha realizado un pedido con el ID {pedido.id}.'
                crear_log_sistema(request.user.username, 'Realizar pedido', detalle, 'Pedidos')
            return JsonResponse({'status': 'success', 'ids': ids})
        
    if usuario.cargo == 'Encargado_oficina':
        if request.method == 'GET':
            ids = request.GET.getlist('id')
            numero = generar_numero_unico()
            for id in ids:
                pedido= get_object_or_404(Pedido, pk=id)
                pedido.estado_de_pedido='realizado'
                pedido.numero_pedido=numero
                pedido.aprobado_oficina= True
                pedido.save()
                autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
                autorizacion_pedido.save()
                enviar_notificacion_pedido(pedido)
                detalle = f'El usuario {request.user.username} ha realizado un pedido con el ID {pedido.id}.'
                crear_log_sistema(request.user.username, 'Realizar pedido', detalle, 'Pedidos')
            return JsonResponse({'status': 'success', 'ids': ids})
    
    if request.method == 'GET':
        ids = request.GET.getlist('id')
        numero = generar_numero_unico()
        for id in ids:
            pedido= get_object_or_404(Pedido, pk=id)
            pedido.estado_de_pedido='realizado'
            pedido.numero_pedido=numero
            pedido.save()
            enviar_notificacion_pedido(pedido) 
            detalle = f'El usuario {request.user.username} ha realizado un pedido con el ID {pedido.id}.'
            crear_log_sistema(request.user.username, 'Realizar pedido', detalle, 'Pedidos')   
        return JsonResponse({'status': 'success', 'ids': ids})
    
    # Si la solicitud no es GET, retorna un error
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

#------------------------------
@login_required
def listar_pedidos_usuarios_almacen(request):
    pagina_actual = request.GET.get('page', 10)
    pedidos_unidad = Pedido.objects.filter(
        aprobado_oficina=True,
        aprobado_unidad=True,
        
        aprobado_cardista = True,
        aprobado_presupuestos = True,
    ).order_by('numero_pedido')
    pedidos_unicos = {}
    for pedido in pedidos_unidad:
        if pedido.numero_pedido not in pedidos_unicos:
            pedidos_unicos[pedido.numero_pedido] = pedido

    pedidos_unicos_list = list(pedidos_unicos.values())
    pedidos_unicos_list=paginador_general(request, pedidos_unicos_list, pagina_actual)

    context = {
        'data': pedidos_unicos_list
    }

    return render(request, 'pedidos/listar_pedido.html', context)

    


@login_required
def listando_pedido_almacen(request, numero):
    pedido= Pedido.objects.filter(numero_pedido=numero)
    context = {
        'data': pedido
    }
    return render(request, 'pedidos/listando.pedidos.almacen.html', context)


@login_required
def lista_pedido_por_id(request, id_pedido):
    pedido=get_object_or_404(Pedido, pk= id_pedido)
    data ={
        'id':pedido.id,
        'codigo':pedido.material.codigo,
        'nombre': pedido.material.nombre,
        'cantidad': pedido.cantidad_pedida,
        'subcantidad': pedido.sub_cantidad_pedida,
        'material':pedido.material.id
        
    }
    return JsonResponse({'data':data})

@login_required
def realizar_entrega(request):
    if request.method == 'POST':
        id= request.POST['pedido_id']
        cantidad_entregada = request.POST['cantidad_entregada']
        if not cantidad_entregada:
            return JsonResponse({'error':'Campo obligatorio'})
        pedido = get_object_or_404(Pedido,pk= id)
        if(pedido.cantidad_entrega > 0):
                return JsonResponse({'data':f'Este pedido ya fue realizada'})
        if(pedido.sub_cantidad_pedida > 0):
        
            if int(cantidad_entregada) < 1:
                return JsonResponse({'data':'Cantidad minima es: 1'})
            elif int(cantidad_entregada) > pedido.sub_cantidad_pedida:
                return JsonResponse({'data':f'Cantidad maxima es:{pedido.sub_cantidad_pedida}'})
        
            cantidad_pedida = pedido.sub_cantidad_pedida - int(cantidad_entregada)
            total_stock = pedido.material.stock
            nuevo_stock = total_stock + cantidad_pedida
            pedido.fecha_entrega_salida = datetime.now()
            pedido.cantidad_entrega = cantidad_entregada
            pedido.estado_pedido_almacen ='Completada'
            pedido.material.stock = nuevo_stock
            pedido.save()
            pedido.material.save()
            detalle = f'El usuario {request.user.username} ha realizado la entrega del pedido con el ID {pedido.id}.'
            crear_log_sistema(request.user.username, 'Entrega de pedido', detalle, 'Pedidos')
            return JsonResponse({'data':'Enviado'})
        

        if int(cantidad_entregada) < 1:
            return JsonResponse({'data':'Cantidad minima es: 1'})
        elif int(cantidad_entregada) > pedido.cantidad_pedida:
            return JsonResponse({'data':f'Cantidad maxima es:{pedido.cantidad_pedida}'})
        
        cantidad_pedida = pedido.cantidad_pedida - int(cantidad_entregada)
        total_stock = pedido.material.stock
        nuevo_stock = total_stock + cantidad_pedida
        pedido.fecha_entrega_salida = datetime.now()
        pedido.cantidad_entrega = cantidad_entregada
        pedido.estado_pedido_almacen ='Completada'
        pedido.material.stock = nuevo_stock
        pedido.save()
        pedido.material.save()
        detalle = f'El usuario {request.user.username} ha realizado la entrega del pedido con el ID {pedido.id}.'
        crear_log_sistema(request.user.username, 'Entrega de pedido', detalle, 'Pedidos')
        return JsonResponse({'data':'Enviado'})

@login_required
def mis_pedidos(request): #muestra los pedidos de cada unidad o secretaria
    pagina_actual = request.GET.get('page', 10)
    pedidos= lista_pedidos_por_estado(request, 'realizado')
    pedidos= paginador_general(request, pedidos, pagina_actual)
    context={
        'data':pedidos,
        'title':'Mis pedidos'   
    }
    return render(request, 'pedidos/mis_pedidos.html', context)

@login_required
def lista_pedidos_por_estado(request,estado):
    id_usuario= request.user.id
    pedidos= Pedido.objects.select_related('usuario').filter(usuario_id=id_usuario, estado_de_pedido=estado).order_by('-fecha_pedido')
    return pedidos

@login_required
def mostrar_informacion_pedidio_aprobaciones(request,id_pedido):
    if request.method == 'GET':
        data=[]
        pedido = get_object_or_404(Pedido, pk=id_pedido)
        aprobaciones = Autorizacion_pedido.objects.filter(pedido= pedido.id)
        for aprobacion in aprobaciones:
            informacion ={
            'unidad':aprobacion.usuario.unidad.nombre,
            'aprobacion':aprobacion.estado_autorizacion,
            'nombre':aprobacion.usuario.persona.nombre + " " + aprobacion.usuario.persona.apellidos ,
            'oficina':aprobacion.usuario.cargo,
            'fecha': aprobacion.fecha_de_autorizacion.strftime('%Y-%m-%d') if aprobacion.fecha_de_autorizacion else None
            }
            data.append(informacion)
        print(data)
        return JsonResponse({'data':data})

@login_required
def eliminar_mi_pedido(request, id_pedido):
    pedido= get_object_or_404(Pedido, pk=id_pedido)
    cantidad=pedido.cantidad_pedida
    stock= pedido.material.stock
    nuevo_stock= stock + cantidad
    print(nuevo_stock)
    pedido_autorizado = Autorizacion_pedido.objects.filter(pedido=pedido)
    for p in pedido_autorizado:
        if p.estado_autorizacion == True:
            return redirect(f"{reverse('mis_pedidos')}?error=Este pedido ha sido aprobado y no se puede cancelar")
        continue
    pedido.material.stock= nuevo_stock
    pedido.material.save()
    pedido.delete()
    detalle = f'El usuario {request.user.username} ha cancelado el pedido con el ID {pedido.id}.'
    crear_log_sistema(request.user.username, 'Cancelación de pedido', detalle, 'Pedidos')
    return redirect(f"{reverse('mis_pedidos')}?success=Pedido cancelado correctamente")

@login_required
def eliminar_mi_pedido_carrito(request, id_pedido):
    pedido= get_object_or_404(Pedido, pk=id_pedido)
    cantidad=pedido.cantidad_pedida
    stock= pedido.material.stock
    nuevo_stock= stock + cantidad
    pedido.material.stock= nuevo_stock
    pedido.material.save()
    pedido.delete()
    detalle = f'El usuario {request.user.username} ha cancelado el pedido con el ID {pedido.id}.'
    crear_log_sistema(request.user.username, 'Cancelación de pedido', detalle, 'Pedidos')
    return redirect(f"{reverse('index')}?success=Pedido cancelado correctamente")

@login_required
def todos_mis_pedidos(request):
    id_usuario= request.user.id
    print(id_usuario)
    pedidos= Pedido.objects.select_related('usuario', 'material').filter(usuario_id=id_usuario).order_by('-fecha_pedido')
    context={
        'data':pedidos,
        'title':'Historial de pedidos'
    }
    return render(request, 'pedidos/mis_pedidos.html', context)


@login_required
def listar_pedidos_cardista(request, ):#admisnitrativo
    pagina_actual = request.GET.get('page', 10)
    pedidos_unidad = Pedido.objects.filter(
        #usuario__unidad=usuario.unidad,
        aprobado_unidad=True,
        aprobado_oficina=True,
    
    ).order_by('numero_pedido')
    pedidos_unicos = {}
    for pedido in pedidos_unidad:
        if pedido.numero_pedido not in pedidos_unicos:
            pedidos_unicos[pedido.numero_pedido] = pedido

    pedidos_unicos_list = list(pedidos_unicos.values())
    pedidos_unicos_list = paginador_general(request,pedidos_unicos_list, pagina_actual)
    context = {
        'data': pedidos_unicos_list
    }
    return render(request, 'pedidos/usuarios.cardista.html', context)


@login_required
def listar_pedidos_presupuestos(request):#admisnitrativo
    pagina_actual = request.GET.get('page', 10)
   
    pedidos_unidad = Pedido.objects.filter(
        #usuario__unidad=usuario.unidad,
        aprobado_unidad=True,
        aprobado_oficina=True,
           aprobado_cardista=True,
    ).order_by('numero_pedido')
    pedidos_unicos = {}
    for pedido in pedidos_unidad:
        if pedido.numero_pedido not in pedidos_unicos:
            pedidos_unicos[pedido.numero_pedido] = pedido

    pedidos_unicos_list = list(pedidos_unicos.values())
    pedidos_unicos_list = paginador_general(request,pedidos_unicos_list, pagina_actual)
    context = {
        'data': pedidos_unicos_list
    }
    return render(request, 'pedidos/usuarios.presupuestos.html', context)


@login_required
def listar_pedidos_unidad(request, id_usuario):#admisnitrativo
    pagina_actual = request.GET.get('page', 10)
    usuario = get_object_or_404(Usuario, pk=id_usuario)#descomentar cuando se quiera recibir por unidad 
    pedidos_unidad = Pedido.objects.filter(
        #usuario__unidad=usuario.unidad,
        aprobado_oficina=True
    ).order_by('numero_pedido')
    pedidos_unicos = {}
    for pedido in pedidos_unidad:
        if pedido.numero_pedido not in pedidos_unicos:
            pedidos_unicos[pedido.numero_pedido] = pedido

    pedidos_unicos_list = list(pedidos_unicos.values())
    pedidos_unicos_list = paginador_general(request,pedidos_unicos_list, pagina_actual)
    context = {
        'data': pedidos_unicos_list
    }
    return render(request, 'pedidos/usuarios.pedidos.html', context)


@login_required
def listar_pedidos_oficina(request, id_usuario):
    pagina_actual = request.GET.get('page', 10)
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    pedidos_unidad = Pedido.objects.filter(
        usuario__oficina=usuario.oficina
    ).order_by('numero_pedido')

    pedidos_unicos = {}
    for pedido in pedidos_unidad:
        if pedido.numero_pedido not in pedidos_unicos:
            pedidos_unicos[pedido.numero_pedido] = pedido

    pedidos_unicos_list = list(pedidos_unicos.values())
    pedidos_unicos_list = paginador_general(request,pedidos_unicos_list, pagina_actual)

    context = {
        'data': pedidos_unicos_list
    }

    return render(request, 'pedidos/usuarios.pedidos.oficina.html', context)

@login_required
def listar_pedidos_por_codigo(request, numero):#listado por unidad
    pedido= Pedido.objects.filter(numero_pedido=numero)
    context = {
        'data': pedido
    }
    return render(request, 'pedidos/listar_pedidos_unidad.html', context)

@login_required
def listar_pedidos_por_codigo_cardista(request, numero):#listado por unidad
    pedido= Pedido.objects.filter(numero_pedido=numero)
    context = {
        'data': pedido
    }
    return render(request, 'pedidos/listar_pedidos_cardista.html', context)

@login_required
def listar_pedidos_por_codigo_presupuesto(request, numero):#listado por unidad
    pedido= Pedido.objects.filter(numero_pedido=numero)
    context = {
        'data': pedido
    }
    return render(request, 'pedidos/listar_pedidos_presupuestos.html', context)


@login_required
def listar_pedidos_por_codigo_oficina(request, numero): #listado por oficina
    pedido= Pedido.objects.filter(numero_pedido=numero)
    context = {
        'data': pedido
    }
    return render(request, 'pedidos/listar_pedidos_oficina.html', context)

@login_required
def autorizar_pedidos(request, id_pedido):#autoria el pedido de cada unidad
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    numero=pedido.numero_pedido
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_unidad= True
    pedido.save()
    url = reverse('pedido_numero', kwargs={'numero': numero})
    return redirect(f"{url}?success=Pedido autorizado correctamente")

@login_required
def autorizar_pedidos_cardista(request, id_pedido):#autoria el pedido de cada unidad
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    numero=pedido.numero_pedido
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_cardista= True
    pedido.save()
    url = reverse('pedido_numero_cardista', kwargs={'numero': numero})
    return redirect(f"{url}?success=Pedido autorizado correctamente")
@login_required
def autorizar_pedidos_presupuestos(request, id_pedido):#autoria el pedido de cada unidad
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    numero=pedido.numero_pedido
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_presupuestos = True
    pedido.save()
    url = reverse('listar_pedidos_por_codigo_presuopuesto', kwargs={'numero': numero})
    return redirect(f"{url}?success=Pedido autorizado correctamente")

@login_required
def autorizar_pedidos_oficina(request, id_pedido):#autoria el pedido de cada unidad

    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    numero=pedido.numero_pedido
    
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_oficina= True
    pedido.save()
    url = reverse('pedido_numero_oficina', kwargs={'numero': numero})
    return redirect(f"{url}?success=Pedido autorizado correctamente")
   
@login_required
def autorizar_pedidos_almacen(request, id_pedido):#autoriza pedidos el lamacen
    user = request.user
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    #usuario = get_object_or_404(Usuario, pk= id_usuario)
   
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= user, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_almacen= True
    pedido.save()
    return redirect('informacion_pedido', pedido.numero_pedido)


@login_required
def rechazar_pedido_unidad(request, id_pedido):
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    pedido.aprobado_unidad= False
    pedido.save()
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= False)
    autorizacion_pedido.save()
    detalle = f'El usuario {request.user.username} ha rechazado el pedido con el ID {pedido.id}.'
    crear_log_sistema(request.user.username, 'Rechazo de pedido', detalle, 'Pedidos')

    return redirect(f"{reverse('listar_pedidos_unidad', kwargs={'id_usuario': id_usuario})}?pedido_rechazado=Pedido rechazado correctamente")
    
    
@login_required
def rechazar_pedido_cardista(request, id_pedido):
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    pedido.aprobado_cardista= False
    pedido.save()
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= False)
    autorizacion_pedido.save()
    detalle = f'El usuario {request.user.username} ha rechazado el pedido con el ID {pedido.id}.'
    crear_log_sistema(request.user.username, 'Rechazo de pedido', detalle, 'Pedidos')

    return redirect(f"{reverse('listar_pedidos_unidad', kwargs={'id_usuario': id_usuario})}?pedido_rechazado=Pedido rechazado correctamente")
    




@login_required
def imprecion_solicitud(request,numero):
    pedido= Pedido.objects.filter(numero_pedido=numero)

    user_pedido = f"{pedido[0].usuario.persona.nombre} { pedido[0].usuario.persona.apellidos }" 
    autorizacion= Autorizacion_pedido.objects.filter(pedido=pedido[0].id)
    user_oficina=None
    user_unidad=None
    user_almacen=None
    for usuarios  in autorizacion:
        print(usuarios.usuario.oficina)
        if usuarios.usuario.cargo == 'Encargado_oficina':
            user_oficina = f"{usuarios.usuario.persona.nombre} { usuarios.usuario.persona.apellidos }" 
        elif usuarios.usuario.cargo == 'Encargado_unidad':
            user_unidad = f"{usuarios.usuario.persona.nombre} { usuarios.usuario.persona.apellidos }" 
        elif usuarios.usuario.oficina.nombre == 'Almacenes':
            user_almacen=  f"{usuarios.usuario.persona.nombre} { usuarios.usuario.persona.apellidos }" 

    context = {
        'data': pedido,
        'usuario_pedido':user_pedido,
        'user_oficina':user_oficina ,
        'user_unidad':user_unidad,
        'user_almacen':user_almacen

    }
    return render(request, "imprimir/solicitud.html", context)



@login_required
def generate_pdf(request, numero):
    pedido= Pedido.objects.filter(numero_pedido=numero)

    user_pedido = f"{pedido[0].usuario.persona.nombre} { pedido[0].usuario.persona.apellidos }" 
    autorizacion= Autorizacion_pedido.objects.filter(pedido=pedido[0].id)
    user_oficina=None
    user_unidad=None
    user_almacen=None
    for usuarios  in autorizacion:
        print(usuarios.usuario.oficina)
        if usuarios.usuario.cargo == 'Encargado_oficina':
            user_oficina = f"{usuarios.usuario.persona.nombre} { usuarios.usuario.persona.apellidos }" 
        elif usuarios.usuario.cargo == 'Encargado_unidad':
            user_unidad = f"{usuarios.usuario.persona.nombre} { usuarios.usuario.persona.apellidos }" 
        elif usuarios.usuario.oficina.nombre == 'Almacenes':
            user_almacen=  f"{usuarios.usuario.persona.nombre} { usuarios.usuario.persona.apellidos }" 

    context = {
        'data': pedido,
        'usuario_pedido':user_pedido,
        'user_oficina':user_oficina ,
        'user_unidad':user_unidad,
        'user_almacen':user_almacen

    }
    html_string = render_to_string('imprimir/solicitud.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedido_materiales.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response



@login_required
def sub_pedido(request):
    pedido= request.POST['pedido']
    sub_pedido= request.POST['sub_pedido']
    material= request.POST['material']
    material_existente= get_object_or_404(Materiales, pk=material)
    if not sub_pedido:
          return JsonResponse({'data':'Ingrese un valor'})

    if int(sub_pedido) <= 0:
        return JsonResponse({'data':'No se puede asignar material menor a 0'})
    if int(sub_pedido) > material_existente.stock:
        return JsonResponse({'data':'No se puede asignar material mayor al stock'})
    pedido = get_object_or_404(Pedido, pk= pedido)
    


    pedido.sub_cantidad_pedida= sub_pedido

    cantidad_p= pedido.cantidad_pedida
    
    material_existente.stock += cantidad_p
    stock= material_existente.stock - int(sub_pedido)
    material_existente.stock=stock
    material_existente.save()
    pedido.save()
    detalle = f'El usuario {request.user.username} ha modificado la cantidad del pedido con el ID {pedido.id}.'
    crear_log_sistema(request.user.username, 'Modificación de pedido', detalle, 'Pedidos')

    return JsonResponse({'data':'guardado'})
@login_required
def sub_pedido_almacen(request):
    pedido = request.GET.get('id_pedido')
    sub_pedido = request.GET.get('cantidad')
    
    material= request.GET.get('material')
    material_existente= get_object_or_404(Materiales, pk=material)
    if not sub_pedido:
          return JsonResponse({'data':'Ingrese un valor'})
    if int(sub_pedido) <= 0:
        return JsonResponse({'data':'No se puede asignar material menor a 0'})
    if int(sub_pedido) > material_existente.stock:
        return JsonResponse({'data':'No se puede asignar material mayor al stock'})
    pedido = get_object_or_404(Pedido, pk= pedido)
    
    pedido.sub_cantidad_pedida= sub_pedido

    cantidad_p= pedido.cantidad_pedida
    
    material_existente.stock += cantidad_p
    stock= material_existente.stock - int(sub_pedido)
    material_existente.stock=stock
    material_existente.save()
    pedido.save()
    
    return JsonResponse({'data':'guardado'})


@login_required
def reporte_pedidos(request):
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']

        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
      
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)

        
        pedidos = Pedido.objects.filter(
            fecha_entrega_salida__gte=fecha_inicio_dt,
            fecha_entrega_salida__lte=fecha_fin_dt
        )
        context={
            'fecha_inicio':fecha_inicio,
            'fecha_fin':fecha_fin,
             'data':pedidos
        }
        
        return render(request, 'pedidos/reporte.pedidos.html', context )

    return render(request, 'pedidos/reporte.pedidos.html')



def reporte_pedido_salida(request):
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']

        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        salida = Pedido.objects.filter(
            fecha_entrega_salida__gte= fecha_inicio_dt,
            fecha_entrega_salida__lte= fecha_fin_dt,
            
        )
        context={
            'fecha_inicio':fecha_inicio,
            'fecha_fin':fecha_fin,
            'data':salida
        }
        return render(request, 'pedidos/reporte.pedidos.salida.html', context)


    return render(request, 'pedidos/reporte.pedidos.salida.html')