from django.urls import path

from log_parser_app import views

urlpatterns = [
    path('', views.index, name='index')
]

