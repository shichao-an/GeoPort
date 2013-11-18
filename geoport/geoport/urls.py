from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'portal.views.index', name='portal'),
    # url(r'^geoport/', include('geoport.foo.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('social.apps.django_app.urls', namespace='social')),

)
