from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='portal'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^groups/', include('groups.urls', namespace='groups')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^friends/', include('friends.urls', namespace='friends')),
    url(r'^user/(?P<username>[\w.@+-]+)/$', 'accounts.views.user', name='user'),

    # Third-party URL includes
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('favicon.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
