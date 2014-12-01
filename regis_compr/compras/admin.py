from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from .models import Proveedores, ProductProvee, CategoriaProducto , Factura, ComprasHechas
from .forms import ComprasHechasForm

class ProductProveeAdmin(admin.TabularInline):
    model = ProductProvee

class ComprasHechasAdmin(ModelAdmin):
  form = ComprasHechasForm

admin.site.register(CategoriaProducto)

site.register(ComprasHechas, ComprasHechasAdmin)

admin.site.register(Proveedores)
admin.site.register(ProductProvee)
admin.site.register(Factura)
