from django.conf.urls import url
from .views import ProveedoresList, ProveedoresDetail, ProveedoresCreate, ProveedoresUpdate, ProveedoresDelete,  ProductProveeCreate, ProductProveeList, ProductProveeDetail, CompradoresCreate, CompradoresDetail
from . import views

urlpatterns = [
	url(r'^add/producto/$', views.add_product_view , name= "vista_agregar_producto"),
	url(r'^edit/producto/(?P<id_prod>.*)/$', views.edit_product_view ,name= "vista_editar_producto"),
    url(r'^buy/producto/(?P<id_prod>.*)/$', views.compra_view, name= "comprar_producto"),
    url(r'^getcart/$', views.get_carrito_compras, name= "get_carrito"),
    url(r'^clean-cart/$', views.borrar_carrito, name= "borrar_carrito"),
    url(r'^finish-buy/$', views.real_compra, name= "visualizar_compra"),
    #to erase
    url(r'^topdf/$', views.to_pdf, name= "to_pdf"),
    url(r'^search-ruc/$', views.search_ruc, name="search_ruc"),
    url(r'^search/$', views.search, name="search"),
    url(r'^proveedor/create$', ProveedoresCreate.as_view(), name='proveedor_create'),
    url(r'^proveedor/list/$', ProveedoresList.as_view(), name='proveedor_list'),
    url(r'^proveedor(?P<pk>\d+)/Update$', ProveedoresUpdate.as_view(), name='proveedor_update'),
    url(r'^proveedor(?P<pk>\d+)/Delete$', ProveedoresDelete.as_view(), name='proveedor_delete'),
    url(r'^proveedor(?P<pk>\d+)$', ProveedoresDetail.as_view(), name='proveedor_detail'),
    url(r'^product/proveedor/create/$', ProductProveeCreate.as_view(), name='product_provee_create'),
    url(r'^producto/proveedor/list/$', ProductProveeList.as_view(), name='produc_provee_list'),
    url(r'^producto_proveedor(?P<pk>\d+)$', ProductProveeDetail.as_view(), name='product_provee_detail'),
    url(r'^comprador/create/$', CompradoresCreate.as_view(), name='comprador_create'),
    url(r'^comprador(?P<pk>\d+)$', CompradoresDetail.as_view(), name='comprador_detail'),
]
