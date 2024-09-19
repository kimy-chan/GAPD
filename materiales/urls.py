from django.urls import path
from .views import crear_categoria,anadir_nuevo_cantidad,eliminar_categoria,actualizar_categoria,listar_categoria_id ,crear_material, listado_material,informacion_material, softDelete, editar_material, inprimir
urlpatterns = [
    path('crear_categoria', crear_categoria, name='crear_categoria'),
      path('crear_material', crear_material, name='crear_material'), 

    path('<int:id_categoria>', listado_material, name='categorias_por_id'),  #ruta para listar los prodcutos por categoria  
    path('informacion/<int:id_material>',informacion_material, name='informacion_material' ),
     path('eliminar/<int:id_material>/<int:id_categoria>',softDelete, name='eliminar' ),
      path('editar_material/<int:id_material>',editar_material, name='editar_material' ),

      path('imprimi/<int:id>', inprimir, name='imprimir' ),
           path('eliminar/<int:id>', eliminar_categoria, name='eliminar_categoria' ),
         path('listar_categoria_id/<int:id>', listar_categoria_id, name='listar_categoria_id' ),
              path('actualizar_categoria', actualizar_categoria, name='actualizar_categoria' ),
                path('anadir/cantidad',anadir_nuevo_cantidad , name='anadir_cantidad' )

]
