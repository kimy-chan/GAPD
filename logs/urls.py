from django.contrib import admin
from django.urls import include, path
from .views import log_materiales,log_categorias,log_usuarios

urlpatterns = [
  path('log/material', log_materiales , name='logs_material'),
    path('log/categorias', log_categorias , name='logs_categorias'),
       path('log/usuarios', log_usuarios , name='logs_usuarios')
]
