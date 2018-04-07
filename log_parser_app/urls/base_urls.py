from django.conf.urls import url

from log_parser_app import views

app_name = 'log_parser_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup_init/$', views.signup_init, name='signup_init'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin_init/$', views.signin_init, name='signin_init'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^details_create/$', views.details_create, name='details_create'),
    url(r'^project_create/$', views.project_create, name='project_create'),
    url(r'^bug_create/$', views.bug_create, name='bug_create'),
    url(r'^log_type_create/$', views.log_type_create, name='log_type_create'),
    url(r'^log_content_type_create/$', views.log_content_type_create, name='log_content_type_create'),
    url(r'^log_create_init/$', views.log_create_init, name='log_create_init'),
    url(r'^log_create/$', views.log_create, name='log_create'),
    url(r'^log_details/$', views.log_details, name='log_details'),
]
