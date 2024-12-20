from django.urls import path
from .views import  *
urlpatterns = [
   path('crear', crear_material_compras, name='crear' ),
     path('listar', listar_material_compras, name='listar' ),
          path('secretaria/material', listar_material_compras_user, name='secreatria_material' ),
           
   
]