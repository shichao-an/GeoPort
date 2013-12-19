from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^event/(?P<blog_slug>[\w.@+-]+)/(?P<event_slug>[\w.@+-]+)/$',
        'events.views.event', name='event'),
    url(r'^event/(?P<blog_slug>[\w.@+-]+)/(?P<event_slug>[\w.@+-]+)/edit/$',
        'events.views.edit', name='edit'),
)

