from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^jtui/', include('apps.juketunes_ui.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('apps.accounts.urls')),
    (r'^twitter/', include('apps.remote_control.urls')),
    (r'^', include('apps.remote_control.urls')),
)

# Serve Media via Django if we're running a development site. This is primarily
# used for local development and should never be done in a production
# environment.
if settings.DJANGO_SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )
