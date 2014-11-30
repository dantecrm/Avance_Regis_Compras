# -*- encoding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.db import models

class ClienteManager(BaseUserManager):
    def create_user(self,username,email,password):
        if not username:
            raise ValueError('El Cliente debe tener un nombre de usuario')
        if not password:
            raise ValueError('La contraseña no es valida')
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password):
        if not username:
            raise ValueError('El Cliente debe tener un nombre de usuario')
        if not password:
            raise ValueError('La contraseña no es valida')
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        user.is_superuser = True
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    def get_by_natural_key(self, username):
        return self.get(username=username)

"""
"""

class Cliente(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(unique=True,max_length=100,verbose_name="Usuario")
    nombre = models.CharField(max_length="30",)
    telefono = models.CharField(max_length="20")
    apellidos = models.CharField(max_length="100")
    direccion = models.CharField(max_length="300")
    identificacion = models.CharField(max_length="20",verbose_name="Identificacion(C.C)")
    email = models.EmailField(unique=True,verbose_name="Correo Electronico",blank=True,null=True)
    ciudad = models.CharField(max_length="40")
    fecha_nacimiento = models.DateField(blank=True,null=True)
    is_admin = models.BooleanField(default=False,verbose_name="Es Admin")
    avatar = models.ImageField(upload_to='avatar/')
    is_active = models.BooleanField(default=True)
    objects = ClienteManager()
    empresa = models.CharField(max_length=50, verbose_name="Nombre de la Empresa")
    date_registro = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return "%s %s"%(self.nombre, self.apellidos)

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    def has_perms(self):
        return True

    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.is_superuser

    def get_photo(self):
        if self.avatar == None:
            return None
        else:
            return self.avatar
