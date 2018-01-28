from django.conf.urls import url

from log_parser_app import views

app_name = 'log_parser_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_log/$', views.new_log, name='new_log'),
    url(r'^new_log_append/$', views.new_log_append, name='new_log_append'),
    url(r'^show_log/$', views.show_log, name='show_log'),
]
