from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'groups.views.index', name="index"),
    url(r'^create/$', 'groups.views.create', name="create"),
    url(r'^events/$', 'groups.views.events', name="events"),
    url(r'^personal/$', 'groups.views.personal', name="personal"),
    url(r'^group/(?P<slug>[\w.@+-]+)/$', 'groups.views.group', name='group'),
)
