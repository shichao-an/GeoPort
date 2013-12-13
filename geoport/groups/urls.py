from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'groups.views.index', name="index"),
)
