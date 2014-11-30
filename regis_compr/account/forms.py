# -*- encoding: utf-8 -*-
from django import forms
from datetime import date
from .models import Cliente

class ContactForm(forms.Form):
	Email	= forms.EmailField(widget=forms.TextInput())
	Titulo	= forms.CharField(widget=forms.TextInput())
	Texto	= forms.CharField(widget=forms.Textarea())

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class RegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput())
    email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
    identificacion = forms.CharField(label="Identificacion C.C. ",widget=forms.TextInput())
    ciudad = forms.CharField(label="Ciudad",widget=forms.TextInput())
    nombre = forms.CharField(label="Primer Nombre",widget=forms.TextInput())
    apellidos = forms.CharField(label="Apellidos",widget=forms.TextInput())
    direccion = forms.CharField(label="Direccion",widget=forms.Textarea())
    telefono = forms.CharField(label ="Telefono",widget=forms.TextInput())
    fecha_nacimiento = forms.DateField(label="Fecha de Nacimiento")
    avatar = forms.ImageField()
    password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
    password_two = forms.CharField(label="Confirmar password",widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = Cliente.objects.get(username=username)
        except Cliente.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya existe')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado')

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        f_final = date.today() - fecha
        if (f_final.days/365) <18:
            raise forms.ValidationError("Debes ser mayor de edad")
        else:
            return fecha

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coinciden')

