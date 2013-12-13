from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='portal'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^groups/', include('groups.urls', namespace='groups')),
    url('', include('social.apps.django_app.urls', namespace='social')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
