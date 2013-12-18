from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'groups.views.index', name="index"),
    url(r'^create/$', 'groups.views.create', name="create"),
    url(r'^events/$', 'groups.views.events', name="events"),
    url(r'^personal/$', 'groups.views.personal', name="personal"),
    url(r'^tag/(?P<slug>[\w.@+-]+)/$', 'groups.views.tag', name='tag'),
    url(r'^group/$', 'groups.views.group_index', name='group_index'),
    url(r'^group/(?P<slug>[\w.@+-]+)/$', 'groups.views.group', name='group'),
    url(r'^group/(?P<slug>[\w.@+-]+)/settings$', 'groups.views.settings',
        name='settings'),
)
