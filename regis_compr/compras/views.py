# coding: utf-8
from django.shortcuts import redirect, render, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Proveedores, ProductProvee, Factura, Compradores, ComprasHechas
from .forms import ProveedoresForm, ProductProveeForm, CompradoresForm, ComprasHechasForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template import RequestContext
from datetime import date,timedelta
from django.template import RequestContext
from django.db.models.expressions import F
import django
from wkhtmltopdf.views import PDFTemplateResponse
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives # Enviamos HTML


def search_ruc(request):
    return render(request, 'index.html')

def search(request):
    if 'buscar' in request.GET and request.GET['buscar']:
        buscar = request.GET['buscar']
        proveedores = Proveedores.objects.filter(num_doc__icontains=buscar)
        return render(request, 'search_results.html',
            {'proveedores': proveedores, 'query': buscar})
    else:
        return HttpResponse('Lo sentimos mucho no se encontró el proveedor.')


def edit_product_view(request, id_prod):
    info = "iniciado"
    prod = ProductProvee.objects.get(pk=id_prod)
    if request.method == "POST":
        form = ProductProveeForm(request.POST,request.FILES,instance=prod)
        if form.is_valid():
            edit_prod = form.save(commit=False)
            form.save_m2m()
            edit_prod.status = True
            edit_prod.save()
            info = "Correcto"
            return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
    else:
        form = ProductProveeForm(instance=prod)
    ctx = {'form':form, 'informacion':info}
    return render_to_response('compras/editProducto.html', ctx, context_instance=RequestContext(request))

def add_product_view(request):
	info = "iniciado"
	if request.method == "POST":
		form = ProductProveeForm(request.POST, request.FILES)
		if form.is_valid():
			add = form.save(commit=False)
			add.status = True
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones de ManyToMany
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/producto/%s'%add.id)
	else:
		form = ProductProveeForm()
	ctx = {'form':form,'informacion':info}
	return render_to_response('compras/addProducto.html',ctx,context_instance=RequestContext(request))


def productos_view(request,pagina):
	lista_prod = ProductProvee.objects.filter(status=True) # Select * from ventas_productos where status = True
	paginator = Paginator(lista_prod,1) # Cuantos productos quieres por pagina? = 3
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage):
		productos = paginator.page(paginator.num_pages)
	ctx = {'productos':productos}
	return render_to_response('compras/productos.html',ctx,context_instance=RequestContext(request))

def singleProduct_view(request,id_prod):
	prod = ProductProvee.objects.get(id=id_prod)
	cats = prod.categorias.all() # Obteniendo las categorias del producto encontrado
	ctx = {'producto':prod,'categorias':cats}
	return render_to_response('compras/SingleProducto.html',ctx,context_instance=RequestContext(request))

def compra_view(request,id_prod):
    if request.user.is_authenticated():
        print request.user
        p = ProductProvee.objects.get(id=id_prod)
        print "p: %s "  % p
        dic = request.session["carrito_de_compra"]
        keys = dic.keys()
        if not p.nombre in keys:
            dic[p.nombre] = [1,p]
        else:
            dic[p.nombre] = [dic[p.nombre][0]+1,p]
        request.session['carrito_de_compras'] = dic
        print "diccionario: %s" % dic
        return HttpResponseRedirect('/productos/page/1/')
    else:
        return HttpResponseRedirect('/login/')

def get_carrito_compras(request):
    productos = request.session["carrito_de_compra"]
    return render_to_response("compras/c_compra.html",{"productos":productos},context_instance=RequestContext(request))

def borrar_carrito(request):
    dic = {}
    request.session["carrito_de_compra"] = dic
    return render_to_response("compras/c_compra.html",{"productos":dic},context_instance=RequestContext(request))


def real_compra(request):
    c_compra = request.session["carrito_de_compra"]
    print "c_compra: %s" % c_compra
    vtotal = 0
    igv = 0
    bas_imp = 0
    f = ComprasHechas.objects.count() + 1
    for key,value in c_compra.items():
        p_pro = value[1].precio
        igv = value[1].igv
        p_total = (float(p_pro)*(1+igv))*float(value[0])
        value.append(p_total)
        vtotal += p_total
    print "vtotal: %s" % vtotal
    igv = (vtotal/1.18)*0.18
    print "igv: %s" % igv
    bas_imp = vtotal/1.18
    print "Base Imponible: %s" % bas_imp
    fecha = date.today()
    return render_to_response("compras/regis_compr_add.html",{"vtotal":vtotal,"productos":c_compra,"igv":igv,"bas_imp":bas_imp, "fecha":fecha,"nf":f},context_instance=RequestContext(request))

def to_pdf(request):
    c_compra = request.session["carrito_de_compra"] #obtengo el carrito de compras de la session
    vtotal = 0 # valor donde acumulare el monto total a pagar por el usuario
    f = Factura.objects.count() + 1 #obtengo el numero de facturas existentes y le sumo uno, como un preview del n de la fact.
    for key,value in c_compra.items(): # el carrito es un diccionario, lo recorro key= nombre del producto
                                       # el value es una lista donde la pos 0 es la cantidad y la pos 1 el producto
        p_pro = value[1].precio # obtengo el valor del producto
        iva = value[1].igv # obtengo el iva aplicado al producto
        p_total = (float(p_pro)*(1+iva))*float(value[0]) # obtengo el valor total del producto x iva x cantidad
        value.append(p_total) # agrego al final de la lista (value) del diccionario el valor total
        vtotal += p_total # sumatoria de los valores totales
    fecha = date.today() # obtengo la fecha de hoy
    return PDFTemplateResponse(request,"compras/facturapdf.html",{"vtotal":vtotal,"productos":c_compra,"fecha":fecha,"nf":f})

class ProveedoresList(ListView):
    template_name = 'compras/proveedores_list.html'
    model = Proveedores

class ProveedoresDetail(DetailView):
    # template_name = 'compras/proveedores_detail.html'
    model = Proveedores
    def dispatch(self, *args, **kwargs):
        return super(ProveedoresDetail, self).dispatch(*args, **kwargs)

class ProveedoresCreate(CreateView):
    # template_name = 'compras/proveedores_create.html'
    model = Proveedores
    form_class = ProveedoresForm
    def dispatch(self, *args, **kwargs):
        return super(ProveedoresCreate, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.object)

class ProveedoresUpdate(UpdateView):
    # template_name = 'compras/proveedores_create.html'
    model = Proveedores
    form_class = ProveedoresForm
    def dispatch(self, *args, **kwargs):
        return super(ProveedoresUpdate, self).dispatch(*args, **kwargs)

class ProveedoresDelete(DeleteView):
    model = Proveedores
    def dispatch(self, *args, **kwargs):
        return super(ProveedoresDelete, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('proveedor_list')

class ProductProveeList(ListView):
    template_name = 'compras/produc_list.html'
    model = ProductProvee

class ProductProveeCreate(CreateView):
    template_name ='compras/produc_provee_create.html'
    model = ProductProvee
    form_class = ProductProveeForm
    def dispatch(self, *args, **kwargs):
        return super(ProductProveeCreate, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.object)

class ProductProveeDetail(DetailView):
    template_name = 'compras/produc_proveed_detail.html'
    model = ProductProvee
    def dispatch(self, *args, **kwargs):
        return super(ProductProveeDetail, self).dispatch(*args, **kwargs)

class CompradoresCreate(CreateView):
    template_name = 'compras/compradores_create.html'
    model = Compradores
    form_class = CompradoresForm
    def dispatch(self, *args, **kwargs):
        return super(CompradoresCreate, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.object)

class CompradoresDetail(DetailView):
    template_name = 'compras/compradores_detail.html'
    model = Compradores
    def dispatch(self, *args, **kwargs):
        return super(CompradoresDetail, self).dispatch(*args, **kwargs)


class ComprasHechasCreate(CreateView):
    template_name = 'compras/buy_hechas_create.html'
    model = ComprasHechas
    form_class = ComprasHechasForm
    def dispatch(self, *args, **kwargs):
        return super(ComprasHechasCreate, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.object)

class ComprasHechasDetail(DetailView):
    template_name = 'compras/compras_hechas_detail.html'
    model = ComprasHechas
    def dispatch(self, *args, **kwargs):
        return super(ComprasHechasDetail, self).dispatch(*args, **kwargs)

def index_view(request):
    request.session["carrito_de_compra"] = {}
    return render_to_response('account/index.html',context_instance=RequestContext(request))

def about_view(request):
    print "----> "
    print request.session.session_key
    version = django.get_version()
    mensaje = "Esto es un mensaje desde mi vista"
    ctx = {'msg':mensaje,'version':version}
    return render_to_response('account/about.html',ctx,context_instance=RequestContext(request))

def register_view(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('account/thanks_register.html',context_instance=RequestContext(request))
        else:
            ctx = {'form':form}
            return 	render_to_response('account/register.html',ctx,context_instance=RequestContext(request))
    form = UserCreationForm()
    return render_to_response('account/register.html',
                              {'form':form},
                              context_instance=RequestContext(request))

def login_view(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            if form.is_valid:
                usuario = request.POST['username']
                clave = request.POST['password']
                acceso = authenticate(username=usuario, password=clave)
                if acceso is not None:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
                else:
                    mensaje = "Usuario y/o password incorrecto"
    form = AuthenticationForm()
    ctx = {'form':form,'mensaje':mensaje}
    return render_to_response('account/login.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login')
def  logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# class FacturaList(ListView):
#     template_name = "compras/factura_list.html"
#     model = Factura

# class FacturaCreate(CreateView):
#     template_name = 'compras/facturacreate.html'
#     model = Factura
#     form_class = FacturaForm
#     def dispatch(self, *args, **kwargs):
#         return super(FacturaCreate, self).dispatch(*args, **kwargs)
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return redirect(self.object)





# class NtCreditoCreate(CreateView):
#     template_name = 'compras/nt_credito_create.html'
#     model = NtCredito
#     form_class = NtCreditoForm
#     def dispatch(self, *args, **kwargs):
#         return super(NtCreditoCreate, self).dispatch(*args, **kwargs)
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return redirect(self.object)

# class NtDebitoCreate(CreateView):
#     template_name = 'compras/nt_debito_create.html'
#     model = NtDebito
#     form_class = NtDebitoForm
#     def dispatch(self, *args, **kwargs):
#         return super(NtDebitoCreate, self).dispatch(*args, **kwargs)
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return redirect(self.object)





# class FacturaDetail(DetailView):
#     template_name = 'compras/factura_detail.html'
#     model = Factura
#     def dispatch(self, *args, **kwargs):
#         return super(FacturaDetail, self).dispatch(*args, **kwargs)

# class NtCreditoDetail(DetailView):
#     template_name = 'compras/ntcredito_detail.html'
#     model = NtCredito
#     def dispatch(self, *args, **kwargs):
#         return super(NtCreditoDetail, self).dispatch(*args, **kwargs)

# class NtDebitoDetail(DetailView):
#     template_name = 'compras/ntdebito_detail.html'
#     model = NtDebito
#     def dispatch(self, *args, **kwargs):
#         return super(NtDebitoDetail, self).dispatch(*args, **kwargs)

