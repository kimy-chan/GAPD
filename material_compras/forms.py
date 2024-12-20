from django import forms
from .models import Matarial_compras ,Stock_material_compras

class Form_material_compras(forms.ModelForm):
    class Meta:
        model = Matarial_compras
        fields = ['proveedor', 'descripcion', 'unidad_manejo', 'secretaria', 'unidad', 'oficina']
        widgets = {
              'proveedor': forms.Select(attrs={
                'class': 'form-control'
            }),
      
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una descripción',
                'rows': 4
            }),
            'unidad_manejo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la unidad de manejo'
            }),
            'secretaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'unidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'oficina': forms.Select(attrs={
                'class': 'form-control'
            }),
          
        }

class Form_stock_material_compras(forms.ModelForm):
    class Meta:
        model = Stock_material_compras
        fields = ['cantidad', 'costo_unitario', 'factura']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad'
            }),
            'costo_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el costo unitario'
            }),
            'factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de factura'
            }),
        }
