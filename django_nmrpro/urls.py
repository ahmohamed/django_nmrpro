from django.conf.urls import patterns, include, url
from django_nmrpro import views

urlpatterns = [
    url(r'^plugins$', views.proc_plugin),
    url(r'^menu$', views.menu),
    url(r'^spectrum/(?P<url>\S+)$', views.spec_url),
    url(r'^viewSpectrum/(?P<url>\S+)$', views.view_spectrum),
    
    # demo urls. Comment if not needed
    url(r'^coffees_specs$', views.coffees_test),
    url(r'^nmrpro_test/$', views.coffees_view),
]

