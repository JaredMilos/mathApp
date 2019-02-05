from django.conf.urls import url
from . import views 

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^menu$', views.menu),
	url(r'^game$', views.game),
	url(r'^guest$', views.guest),
	url(r'^save_user$', views.save_user),
	url(r'^log_user$', views.log_user),
	url(r'^end_of_round$', views.end_of_round),
	url(r'^clear_counter$', views.clear_counter),
	url(r'^submit_response$', views.submit_response),
	url(r'^rerack$', views.rerack),
	url(r'^flush$', views.flush)
]