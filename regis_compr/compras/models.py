# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings

class Proveedores(models.Model):
    TIPO_DOC = (
	(0, 'OTROS TIPOS DE DOCUMENTOS'),
	(1, 'DOCUMENTO NACIONAL DE IDENTIDAD (DNI)'),
	(4, 'CARNET DE EXTRANJERIA'),
	(6, 'REGISTRO ÚNICO DE CONTRIBUYENTES'),
	(7, 'PASAPORTE')
    )
    proveedor = models.CharField(max_length=30, verbose_name="Nombre o Razón Social")
    tip_doc = models.PositiveSmallIntegerField(choices=TIPO_DOC, default=6)
    num_doc = models.CharField(max_length=11, verbose_name="Número de Documento")
    date_registro = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s %s " %(self.proveedor, self.num_doc)

    @models.permalink
    def get_absolute_url(self):
        return ('proveedor_detail', [int(self.pk)])


class categoriaProducto(models.Model):
    nombre 	= models.CharField(max_length=200)
    descripcion = models.TextField(max_length=400)

    def __unicode__(self):
        return self.nombre

class ProductProvee(models.Model):
    def url(self,filename):
        ruta = "MultimediaData/Producto/%s/%s"%(self.nombre,str(filename))
        return ruta
    nombre = models.CharField(max_length=100, verbose_name="Nombre de Producto")
    proveedor_produc = models.ForeignKey(Proveedores)
    descripcion = models.TextField()
    stock = models.IntegerField()
    status = models.BooleanField(default=True)
    imagen 		= models.ImageField(upload_to=url,null=True,blank=True)
    categorias	= models.ManyToManyField(categoriaProducto,null=True,blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    igv         = models.FloatField()
    date_registro = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s de %s del proveedor %s" %(self.nombre, self.precio, self.proveedor_produc.proveedor)

    @models.permalink
    def get_absolute_url(self):
        return ('product_provee_detail', [int(self.pk)])

class Factura(models.Model):
    total = models.IntegerField()
    comprador = models.ForeignKey(User)
    producto_comprado = models.ManyToManyField(ProductProvee)
    fecha = models.DateField()
    fecha_cambio = models.DateField(verbose_name="Fecha Maxima de retorno")
    def __unicode__(self):
        return u"%s %s"%(self.comprador,self.fecha)

class Compradores(models.Model):
    comprador = models.OneToOneField(User)
    empresa = models.CharField(max_length=50, verbose_name="Nombre de la Empresa")
    direccion = models.CharField(max_length=50, verbose_name="Domicilio Comercial")
    date_registro = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Usuario %s de la empresa %s" %(self.comprador.username, self.empresa)

    @models.permalink
    def get_absolute_url(self):
        return ('comprador_detail', [int(self.pk)])


class ComprasHechas(models.Model):
    comprado = models.ForeignKey(Compradores)
    productos = models.ManyToManyField(ProductProvee)
    publication_date = models.DateField(auto_now=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return "El total de la compra es %s de la empresa %s" %(self.total, self.comprado.empresa)

    @models.permalink
    def get_absolute_url(self):
        return ('comprashechas_detail', [int(self.pk)])

# class Factura(models.Model):
#     codigo_proveedor = models.CharField(max_length=3, verbose_name="Entrada en el diario")
#     ct_asoc = models.CharField(max_length=30, verbose_name="Cuenta Asociada")
#     descuento = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Descuento máximo por pronto pago")
#     fecha_fact = models.DateField(verbose_name="Fecha de Facturación")
#     fecha_venc = models.DateField(verbose_name="Fecha de Vencimiento")
#     num_fact = models.PositiveIntegerField(verbose_name="No. Factura")
#     num_folio = models.CharField(max_length=20, verbose_name="Folio de Venta")
#     rfc = models.CharField(max_length=13, verbose_name="Registro Federal de Contribuyentes")
#     nombre = models.OneToOneField(Compradores)
#     direccion = models.CharField(max_length=50)
#     productos = models.ForeignKey(ComprasHechas)
# #    total = models.DecimalField(max_digits=9, decimal_places=2)
# #    cantidad ==> Es la cantidad total pagada expresada en letra.
# #    subtotal ==> Es la cantidad pagada sin impuesto de los productos o platillos a Facturar.
# #    IVA ==> Cantidad de impuesto de los productos o platillos a facturar.
#     def __unicode__(self):
#        return "Con No de Factura %s el total es %s" %(self.num_fact, self.productos.total)

#     @models.permalink
#     def get_absolute_url(self):
#         return ('factura_detail', [int(self.pk)])

# TIP_COM = (
#     (0,'Otros'),
#     (1,'Factura'),
#     (7,'Nota de Crédito'),
#     (8,'Nota de Débito'),
# )

# class NtCredito(models.Model):
#     STATUS = (
#         (0, 'Pendiente'),
#         (1, 'Pendiente-Impreso'),
#         (2, 'Cancelado'),
#         (3, 'Cerrado'),
#         (4, 'Borrador'),
#     )
#     MONEDA = (
#         (0, 'Soles'),
#         (1, 'Dólares'),
#         (2, 'Euros'),
#         (3, 'Reales'),
#         (4, 'Yenes'),
#         (5, 'Won'),
#         (6, 'Pesos')
#     )

#     persona = models.ForeignKey(Compradores, verbose_name="Persona de contacto")
# #    num_ref = models.PositiveIntegerField(null=True,blank=True, verbose_name="Número de referencia del acreedor")
#     tipo_comp = models.PositiveSmallIntegerField(choices=TIP_COM, default=1, verbose_name="Tipo de Comprobante")
#     num_com = models.ForeignKey(Factura, verbose_name="Número de Comprobante")
#     nit = models.PositiveIntegerField(verbose_name="Nit")
# #    num_izq = models.PositiveIntegerField(verbose_name="Campo de la izquierda(Serie de numeración)")
#     num_der = models.PositiveIntegerField(verbose_name="Campo de la derecha(Número de nota de crédito de proveedores)")
#     status = models.PositiveSmallIntegerField(choices=STATUS, default=2)
#     fecha_cont = models.DateField(verbose_name="Fecha de contabilización")
#     fecha_venc = models.DateField(verbose_name="Fecha de vencimiento")
#     tiempo_registro = models.DateTimeField(auto_now=True, verbose_name="Fecha de documento")
#     moneda = models.PositiveSmallIntegerField(choices=MONEDA, default=0)
#     encargado = models.CharField(max_length=40, verbose_name="Encargado de compras")
#     titular = models.CharField(max_length=40, verbose_name="Empleado Titular de la Nota de Crédito de Proveesores")
#     proveedor = models.ForeignKey(Proveedores)
#     comentarios = models.TextField()
#     total_antes = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total antes del descuento")
#     descuento = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="% de descuento")
# #    anticipo = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Anticipo total")
#     impuesto = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Impuesto")
#     total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Importe Total")

#     def __unicode__(self):
#         return "El comprador %s tiene una ganancia de %s" %(self.persona.comprador.username, self.total)

#     @models.permalink
#     def get_absolute_url(self):
#         return ('ntcredito_detail', [int(self.pk)])

# class NtDebito(models.Model):
#     MOTIVO = (
#         (0, 'Errores de Monto'),
#         (1, 'Facturación'),
#         (2, 'Bonificación'),
#         (3, 'Descuento'),
#         (4, 'Otro'),
#     )

#     MONEDA = (
#         (0, 'Soles'),
#         (1, 'Dólares'),
#         (2, 'Euros'),
#         (3, 'Reales'),
#         (4, 'Yenes'),
#         (5, 'Won'),
#         (6, 'Pesos')
#     )
#     comprador = models.ForeignKey(Compradores)
#     fecha_actual = models.DateTimeField(auto_now=True, verbose_name="Fecha Operación")
#     tipo_comp = models.PositiveSmallIntegerField(choices=TIP_COM, default=1, verbose_name="Tipo de Comprobante")
#     num_comp = models.ForeignKey(Factura)
#     nit = models.PositiveIntegerField(verbose_name="Nit")
#     proveedor = models.ForeignKey(Proveedores)
#     fecha_venc = models.DateField(verbose_name="Fecha de Vencimiento")
#     motivo = models.PositiveSmallIntegerField(choices=MOTIVO, default=0, verbose_name="Motivo de Operación")
#     referencia = models.TextField(verbose_name="Referencia")
#     total_antes = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total antes del descuento")
#     importe = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Monto debitado")
#     moneda = models.PositiveSmallIntegerField(choices=MONEDA, default=0)
#     total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Importe Total")

#     def __unicode__(self):
#         return "Se hizo el importe a su cuentab de %s %s al comprador %s" %(self.importe, self.moneda, self.comprador.comprador.username)

#     @models.permalink
#     def get_absolute_url(self):
#         return ('ntdebito_detail', [int(self.pk)])

# class RegistCompras(models.Model):
#     codig_uni = models.CharField(max_length=5, verbose_name="NÚMERO CORRELATIVO DEL REGISTRO O CÓDIGO UNICO DE LA OPERACIÓN")
#     fecha_emision = models.DateField(verbose_name="FECHA DE EMISIÓN DEL COMPROBANTE DE PAGO O DOCUMENTO")
#     fecha_venci_pago = models.DateField(verbose_name="FECHA DE VENCIMIENTO O FECHA DE PAGO")
#     comprob_pago = models.PositiveSmallIntegerField(choices=TIP_COM, default=1)
#     serie = models.IntegerField(verbose_name="SERIE O CÓDIGO DE LA DEPENDENCIA ADUANERA")
#     anio_emision = models.IntegerField(null=True, blank=True, verbose_name="AÑO DE EMISIÓN DE LA DUA O DSI")
#     no_compr = models.IntegerField(verbose_name="N° DEL COMPROBANTE DE PAGO")
#     inf_proveedor = models.ForeignKey(Proveedores)
#     base_impo = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Base Imponible")
#     igv = models.DecimalField(max_digits=3, decimal_places=2)
#     total = models.DecimalField(max_digits=12, decimal_places=2)

#     def __unicode__(self):
#         return "%s %s" %(self.total, self.inf_proveedor.proveedor)

#     @models.permalink
#     def get_absolute_url(self):
#         return ('regis_compras_detail', [int(self.pk)])
