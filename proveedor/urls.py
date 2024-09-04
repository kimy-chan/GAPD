
from django.urls import path 
from  .views import actulizar_proveedor, softDelete,formulario_proveedor, listar_proveedores
 
urlpatterns = [
    path('', listar_proveedores, name='listar_proveedor'),
    path('añadir_proveedor', formulario_proveedor, name='añadir_proveedor'),
    path('actualizar_proveedor/<int:id>' , actulizar_proveedor, name='actualizar_proveedor'),
        path('eliminar/<int:id>' ,softDelete, name='eliminar'),
    
    
]
