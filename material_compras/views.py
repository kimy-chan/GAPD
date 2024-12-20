from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from material_compras.forms import Form_stock_material_compras, Form_material_compras
from material_compras.models import Matarial_compras

def crear_material_compras(request):
    form_stock = Form_stock_material_compras(request.POST or None)
    form_compras = Form_material_compras(request.POST or None)

    if request.method == 'POST':
        if form_compras.is_valid() and form_stock.is_valid():
            try:   
                secretaria = request.POST.get('secretaria')
                unidad = request.POST.get('unidad')
                oficina = request.POST.get('oficina')
                cantidad = request.POST.get('cantidad')
                costo_unitario = request.POST.get('costo_unitario')

      
                seleccionados = sum(bool(x) for x in [secretaria, unidad, oficina])
                if seleccionados != 1:
                    messages.error(request, "Debe seleccionar solo una opción: secretaria, unidad o oficina.")
                else:
        
                    material = form_compras.save(commit=False)
                
                    material.stock=int(cantidad)
                    if secretaria:
                        material.secretaria_flag = True
                    elif unidad:
                        material.unidad_flag = True
                    elif oficina:
                        material.oficina_flag = True
          
           
             
                    material.save()
                    stock_compras = form_stock.save(commit=False)
                    stock_compras.matarial_compras = material
              
                    stock_compras.costo_total = float(cantidad) * float(costo_unitario)
                    stock_compras.save()
                    messages.success(request, "Material de compras y stock creado exitosamente.")
                    return redirect('crear') 
            except Exception  as error:
                    messages.error(request, "Error inenperado")
               

    context = {
        'form_compras': form_compras,
        'form_stock': form_stock,
    }
    return render(request, 'material_compras/crear.html', context)


def listar_material_compras(request):
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        print(fecha_inicio_dt,fecha_fin_dt)
        material = Matarial_compras.objects.filter(flag=True,            
                                                  fecha_creacion__gte=fecha_inicio_dt,
                              fecha_creacion__lte=fecha_fin_dt)
        context={
            'data':material
        }
        return render(request, 'material_compras/listar.html', context)
    return render(request, 'material_compras/listar.html')

def listar_material_compras_user(request):
    user= request.user
  
    if request.method =='POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
        print(fecha_inicio_dt,fecha_fin_dt)
        material = Matarial_compras.objects.filter(flag=True,            
                                                  fecha_creacion__gte=fecha_inicio_dt,
                              fecha_creacion__lte=fecha_fin_dt,
                              secretaria_flag=True,
                              secretaria=user.unidad.secretaria
                              
                              )
        context={
            'data':material
        }
        return render(request, 'material_compras/secretaria.html', context)
    return render(request, 'material_compras/secretaria.html')