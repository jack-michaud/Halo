from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^queries/$', views.query_view, name='queries'),
    url(r'^queries/(?P<num>[0-9]+)/$', views.query_id, name='query_id'),
    url(r'^graphs/$', views.graph_view_json, name='graph_view_json'),
    url(r'^graphs/(?P<num>[0-9]+)/$', views.graph_id, name='graph_id'),
    url(r'^prepare/$', views.prepare_query, name='prepare'),
    url(r'^make-query/$', views.make_query, name='make_query'),
    url(r'^make-graph/$', views.make_graph, name='make_graph'),
]
