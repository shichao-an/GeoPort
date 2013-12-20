from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/$',
        'events.views.event', name='event'),
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/edit/$',
        'events.views.edit', name='edit'),
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/participate/$',
        'events.views.participate', name='participate'),
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/query/markers/$',
        'events.ajax.markers', name='markers'),
    url(r'^event/(?P<group_slug>[\w.@+-]+)/(?P<event_id>[\w.@+-]+)/query/leave/$',
        'events.ajax.leave', name='leave'),
)

