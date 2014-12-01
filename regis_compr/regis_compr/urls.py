# coding: utf-8
from django.conf.urls import patterns,include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from compras.views import ProveedoresList, ProveedoresDetail, ProveedoresCreate, ProveedoresUpdate, ProveedoresDelete,  ProductProveeCreate, ProductProveeList, ProductProveeDetail, CompradoresCreate, CompradoresDetail, ComprasHechasCreate, ComprasHechasDetail
from compras import views
# from webServices.wsProductos import views
from django.contrib import admin

urlpatterns = patterns('',
    # url(r'^$', TemplateView.as_view(template_name='base.html')),
    # Examples:
    # url(r'^$', 'project_name.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^', include('account.urls')),
    # url(r'^compras/', include('compras.urls')),
    # Buscar Proveedor por RUC

    # Sessión
	url(r'^$', views.index_view,name='vista_principal'),
	url(r'^about/$', views.about_view, name='vista_about'),
	url(r'^login/$', views.login_view,name='vista_login'),
	url(r'^registro/$',views.register_view,name='vista_registro'),
	url(r'^logout/$', views.logout_view,name='vista_logout'),

	url(r'^ws/productos/$', 'webServices.wsProductos.views.wsProductos_view' ,name= "ws_productos_url"),
    # App Compras Operaciones
	url(r'^add/producto/$', views.add_product_view , name= "vista_agregar_producto"),
	url(r'^edit/producto/(?P<id_prod>.*)/$', views.edit_product_view ,name= "vista_editar_producto"),
    url(r'^buy/producto/(?P<id_prod>.*)/$', views.compra_view, name= "comprar_producto"),
    url(r'^getcart/$', views.get_carrito_compras, name= "get_carrito"),
    url(r'^clean-cart/$', views.borrar_carrito, name= "borrar_carrito"),
    url(r'^finish-buy/$', views.real_compra, name= "visualizar_compra"),
    url(r'^topdf/$', views.to_pdf, name= "to_pdf"),
	url(r'^productos/page/(?P<pagina>.*)/$', views.productos_view,name='vista_productos'),
	url(r'^producto/(?P<id_prod>.*)/$',views.singleProduct_view, name='vista_single_producto'),
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
    url(r'^comprashechas/create/$', ComprasHechasCreate.as_view(), name='comprashechas_create'),
    url(r'^comprashechas(?P<pk>\d+)$', ComprasHechasDetail.as_view(), name='comprashechas_detail'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
