from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^registration$', views.registration),
	url(r'^login$', views.login),
	
	
	url(r'^logout$', views.logout),
	url(r'^dashboard$', views.dashboard),
	url(r'^additem$', views.additem),
	url(r'^addwishlist$', views.addwishlist),
	url(r'^removefromlist$', views.removefromlist),
	url(r'^wish_items/(?P<id>\d+)$', views.show_item),
	
	url(r'^wish_items/create$', views.create),
]