from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from .models import Proveedores, ProductProvee, Factura, ComprasHechas
from .forms import ComprasHechasForm

class ComprasHechasAdmin(ModelAdmin):
  form = ComprasHechasForm

site.register(ComprasHechas, ComprasHechasAdmin)

admin.site.register(Proveedores)
admin.site.register(ProductProvee)
admin.site.register(Factura)

