from django import forms
from .models import Proveedores, Compradores, ProductProvee, ComprasHechas
from django.forms import ModelMultipleChoiceField

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        exclude = ['']

class CompradoresForm(forms.ModelForm):
    class Meta:
        model = Compradores
        exclude = ['']

class ProductProveeForm(forms.ModelForm):
    class Meta:
        model = ProductProvee
        exclude = ['status']

class ComprasHechasForm(forms.ModelForm):
    class Meta:
        model = ComprasHechas
        exclude = ['']
    # productos = forms.ModelMultipleChoiceField(queryset=ProductProvee.objects.all())

    # def __init__(self, *args, **kwargs):
    #     if 'instance' in kwargs:
    #         initial = kwargs.setdefault('initial', {})
    #         initial['productos'] = [t.pk for t in kwargs['instance'].productos_set.all()]
    #         forms.ModelForm.__init__(self, *args, **kwargs)

    # def save(self, commit=True):
    #     instance = forms.ModelForm.save(self, False)

    #     old_save_m2m = self.save_m2m
    #     def save_m2m():
    #        old_save_m2m()
    #        instance.productos_set.clear()
    #        for topping in self.cleaned_data['productos']:
    #            instance.productos_set.add(productos)
    #     self.save_m2m = save_m2m

    #     if commit:
    #         instance.save()
    #         self.save_m2m()

        # return instance
# class FacturaForm(forms.ModelForm):
#     class Meta:
#         model = Factura

# class NtCreditoForm(forms.ModelForm):
#     class Meta:
#         model = NtCredito

# class NtDebitoForm(forms.ModelForm):
#     class Meta:
#         model = NtDebito
