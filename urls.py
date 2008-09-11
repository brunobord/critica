"""
URLs for ``critica``.

"""
import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

# Applications
# ------------------------------------------------------------------------------
urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^pages/', include('critica.apps.pages.urls')),
    (r'^rss/', include('critica.apps.syndication.urls')),
    (r'', include('critica.apps.journal.urls')),
)

# Media
# ------------------------------------------------------------------------------
if settings.DEBUG or False:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$',
            'serve',
            dict(
                document_root = os.path.join(settings.PROJECT_PATH, 'media'),
                show_indexes = True
            )
        ),
    )

