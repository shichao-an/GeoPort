from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/$',
        'events.views.event', name='event'),
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/edit/$',
        'events.views.edit', name='edit'),
)

