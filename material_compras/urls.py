from django.urls import path
from .views import  *
urlpatterns = [
   path('crear', crear_material_compras, name='crear' ),
     path('listar', listar_material_compras, name='listar' ),
         path('guradar', guardar_material_compras, name='guardar_material_compras' ),
          path('secretaria/material', listar_material_compras_user, name='secreatria_material' ),
            path('cargar-unidades/', cargar_unidades, name='cargar_unidades'),
    path('cargar-oficinas/', cargar_oficinas, name='cargar_oficinas'),
        path('eliminar/compra/<int:id>', eliminar, name='eliminar'),
   
]