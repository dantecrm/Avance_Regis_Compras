from django.conf.urls import patterns,url


urlpatterns = patterns('account.views',
	url(r'^inicio/$','index_view',name='vista_principal'),
	url(r'^about/$','about_view',name='vista_about'),
	url(r'^contacto/$','contacto_view',name='vista_contacto'),
	url(r'^login/$','login_view',name='vista_login'),
	url(r'^registro/$','register_view',name='vista_registro'),
	url(r'^logout/$','logout_view',name='vista_logout'),
)
