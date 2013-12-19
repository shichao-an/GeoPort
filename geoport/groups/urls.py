from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'groups.views.index', name="index"),
    url(r'^create/$', 'groups.views.create', name="create"),
    url(r'^events/$', 'groups.views.events', name="events"),  # Aggregated
    url(r'^personal/$', 'groups.views.personal', name="personal"),
    url(r'^tag/(?P<slug>[\w.@+-]+)/$', 'groups.views.tag', name='tag'),
    url(r'^group/$', 'groups.views.group_index', name='group_index'),
    url(r'^group/(?P<slug>[\w.@+-]+)/$', 'groups.views.group', name='group'),
    url(r'^group/(?P<slug>[\w.@+-]+)/settings/$', 'groups.views.group_settings',
        name='group_settings'),
    url(r'^group/(?P<slug>[\w.@+-]+)/events/$', 'groups.views.group_settings',
        name='group_events'),
    url(r'^group/(?P<slug>[\w.@+-]+)/events/create/$',
        'events.views.create',
        name='create_event'),
    # Ajax
    url(r'^group/(?P<slug>[\w.@+-]+)/query/admins$',
        'groups.ajax.admins',
        name='admins'),
    url(r'^group/(?P<slug>[\w.@+-]+)/query/join$',
        'groups.ajax.join',
        name='join'),
    url(r'^group/(?P<slug>[\w.@+-]+)/query/quit$',
        'groups.ajax.quit',
        name='quit'),
)
