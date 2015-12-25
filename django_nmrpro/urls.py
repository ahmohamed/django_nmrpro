from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^plugins$', 'django_nmrpro.views.proc_plugin'),
    url(r'^menu$', 'django_nmrpro.views.menu'),
    url(r'^spectrum/(?P<url>\S+)$', 'django_nmrpro.views.spec_url'),
    url(r'^viewSpectrum/(?P<url>\S+)$', 'django_nmrpro.views.view_spectrum'),
    
    # demo urls. Comment if not needed
    url(r'^coffees_specs$', 'django_nmrpro.views.coffees_test'),
    url(r'^nmrpro_test/$', 'django_nmrpro.views.coffees_view'),
)

