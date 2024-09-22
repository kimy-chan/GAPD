
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from logs.views import crear_log_sistema
from .forms import Formulario_categoria,Formulario_materiales,Form_infomacion_material
from django.http import JsonResponse
from django.http import HttpResponse


from django.template.loader import get_template
from .models import Categoria, Materiales, Informacion_material


def crear_categoria(request):    
    if(request.method == 'POST'):
        formulario= Formulario_categoria(request.POST)
        if formulario.is_valid():
            categoria=formulario.save()
            detalle=f'Se ha creado una nueva categoría: {categoria.nombre}'
            crear_log_sistema(request.user.username,'Creación de categoría', detalle ,'Categoria')
            return JsonResponse({'data':True})
        else:
            formulario= Formulario_categoria(request.POST)
            errors=  dict(formulario.errors.items())
            return JsonResponse({'errores':errors})
    else:
        formulario= Formulario_categoria()  
    categorias = Categoria.objects.filter(es_habilitado=True ).order_by('-fecha_creacion')
    context={
        'form':formulario,
        'categorias':categorias
    }
    return render(request, 'materiales/categoria/formulario.crear.html', context)

def crear_material(request):
    if(request.method=='POST'):
        formulario= Formulario_materiales(request.POST)
        formulario_info_material= Form_infomacion_material(request.POST)
        if(formulario.is_valid() and formulario_info_material.is_valid()):
            codigo= formulario.cleaned_data['codigo']
            codigo_paquete= formulario.cleaned_data['codigo_paquete']
            categoria= formulario.cleaned_data['categoria']
            cantidad_paquete= formulario_info_material.cleaned_data['cantidad_paquete']
            cantidad_paquete_unidad= formulario_info_material.cleaned_data['cantidad_paquete_unidad']
            material= formulario.save(commit=False)
            material.codigo_paquete= f"{categoria.codigo_clasificacion}-{codigo_paquete }"
            material.codigo=f"{material.codigo_paquete}-{codigo}"
            material.stock= cantidad_paquete * cantidad_paquete_unidad
            material.save()
            info_material= formulario_info_material.save(commit=False)
            info_material.material= material
            info_material.save()
            info_material.calcular_total_cantidad()
            info_material.calcular_precio_total()
            detalle=f'Se ha creado una nuevo material: {material.nombre} con el codigo {material.codigo}'
            crear_log_sistema(request.user.username,'Creación de Materiales', detalle ,'Materiales')
        else:
            formulario= Formulario_materiales(request.POST)
            formulario_info_material= Form_infomacion_material(request.POST)
    else: 
        formulario= Formulario_materiales()
        formulario_info_material= Form_infomacion_material()
    context={
        'form':formulario,
        'form_info':formulario_info_material
    }
    return render(request, 'materiales/formulario.material.html', context)


def listado_material(request, id_categoria):#lista todos los material por categoria
    listar_productos_categoria= Materiales.objects.select_related('categoria').filter(categoria_id=id_categoria,es_habilitado=True)
    nombre_categoria = Categoria.objects.get(pk=id_categoria)#trae el nombre de la categoria para el sud titulo
    context={
        'data':listar_productos_categoria,
        'nombre_categoria':nombre_categoria
    }
    return render(request, 'materiales/listar_material.html', context)

def informacion_material(request, id_material):
    info_producto= Materiales.objects.get(pk= id_material)
    context={
        'material':info_producto
    }
    return render(request, 'materiales/informacion_material.html', context)

def editar_material(request, id_material):
    material = get_object_or_404(Materiales, pk=id_material)
    formulario_material = Formulario_materiales(request.POST or None, instance= material)
    if request.method == 'POST':
        if formulario_material.is_valid():
            codigo= formulario_material.cleaned_data['codigo']
            codigo_paquete= formulario_material.cleaned_data['codigo_paquete']
            antiguo_codigo_paquete=codigo_paquete.split('-')
            codigo_antiguo=codigo.split('-')
            categoria= formulario_material.cleaned_data['categoria']
            material= formulario_material.save()
            material.codigo_paquete= f"{categoria.codigo_clasificacion}-{antiguo_codigo_paquete[1]}"
            material.codigo=f"{material.codigo_paquete}-{codigo_antiguo[2]} "
            material.save()
          
            detalle = f'Se ha editado el material con el código: {material.codigo}'
            crear_log_sistema(request.user.username,'Edicion de Materiales', detalle ,'Materiales')
            return HttpResponse('actulizado')
    
    context={
        'form':formulario_material,
        'material': material

    }
    return render(request, 'materiales/formulario.actulizar.material.html', context)

def softDelete(request, id_material, id_categoria): #elimina el material
    material = get_object_or_404(Materiales, pk= id_material)
    categoria = get_object_or_404(Categoria, pk= id_categoria)
    material.es_habilitado= False
    material.save()
    detalle = f'Se ha eliminado el material con el código: {material.codigo}'
    crear_log_sistema(request.user.username,'Eliminacion de Materiales', detalle ,'Materiales')
    return  redirect("categorias_por_id", id_categoria=categoria.id)



def inprimir(request, id):
    ruta_tamplate ='materiales/informacion_material.html'
    template = get_template(ruta_tamplate)
    mate = get_object_or_404(Materiales, pk=id)
    context = {'material': mate}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

def listar_categoria_id(request, id):
    categoria= get_object_or_404(Categoria, pk=id)
    data={
        'nombre':categoria.nombre,
        'id':categoria.id
    }
    return JsonResponse(data)

def actualizar_categoria(request):
    id=request.POST['id']
    nombre=request.POST['nombre']
    if not  nombre  or not id:
        return JsonResponse({'error':'Ingrese los campos'})
    categoria= get_object_or_404(Categoria, pk=id)
    nombre_anterior= categoria.nombre
    categoria.nombre =nombre
    categoria.save()
    detalle=f"Se ha editado la categoría: {nombre_anterior} a {categoria.nombre}"
    crear_log_sistema(request.user.username,'Edicion de categoría', detalle ,'Categoria')
    return JsonResponse({'data':True})
def eliminar_categoria(request, id):
    categoria= get_object_or_404(Categoria, pk=id)
    categoria.es_habilitado=False
    categoria.save()
    detalle=f"Se ha Elimando la categoría: {categoria.nombre}"
    crear_log_sistema(request.user.username,'Eliminacion de la categoría', detalle ,'Categoria')
    return redirect('crear_categoria')

def anadir_nuevo_cantidad(request):
    cantidad_unidad= request.POST['cantidadUnidad']
    cantidad_paquete= request.POST['cantidadPaquete']
    precio_paquete= request.POST['precioPaquete']
    id_material=request.POST['materialId']
    precio_unidad=request.POST['precio_unidad']
    if not cantidad_unidad or not cantidad_paquete or not id_material:
        return JsonResponse({'data':'Campos obligatorios'})
    totalCantidad = int(cantidad_unidad) * int(cantidad_paquete)
    material=get_object_or_404(Materiales, pk = id_material)
  
    stock = material.stock
    material.stock= int(stock) + totalCantidad
    
    info_mat = Informacion_material.objects.create(cantidad_paquete= int(cantidad_paquete), cantidad_paquete_unidad= int(cantidad_unidad), precio_unidad=float(precio_unidad),precio_paquete=float(precio_paquete),material= material)
    info_mat.calcular_total_cantidad()
    info_mat.calcular_precio_total()
    material.save()
    info_mat.save()
    detalle = f'Se registro una nueva cantidad al material con el código: {material.codigo}'
    crear_log_sistema(request.user.username,'Adición de Cantidades', detalle ,'Materiales')
    return JsonResponse({'data':True})