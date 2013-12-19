from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'accounts.views.index', name="index"),
    url(r'^login/$', 'accounts.views.login_view', name="login"),
    url(r'^signup/$', 'accounts.views.signup', name="signup"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^profile/$', 'accounts.views.profile', name="profile"),
    url(r'^settings/$', 'accounts.views.settings', name="settings"),
    url(r'^avatar/$', 'accounts.views.avatar', name="avatar"),
    url(r'^email/$', 'accounts.views.email', name="email"),
    url(r'^password/$', 'accounts.views.password', name="password"),
    url(r'^query/users/$', 'accounts.ajax.users', name="users"),
)
