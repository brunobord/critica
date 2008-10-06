"""
URLs of ``critica`` project.

"""
import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.admin.views import basic_dashboard

# Admin
# ------------------------------------------------------------------------------
admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/dashboard/(?P<issue>\d+)/', basic_dashboard),
    (r'^admin/dashboard/', basic_dashboard),
    (r'^admin/(.*)', basic_site.root),
    (r'^advanced-admin/(.*)', advanced_site.root),
    (r'^django-admin/(.*)', admin.site.root),
)

# Applications
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    #(r'^archives/', include('critica.apps.archives.urls')),
    (r'^pages/', include('critica.apps.pages.urls')),
    #(r'^rss/', include('critica.apps.syndication.urls')),
    #(r'', include('critica.apps.categories.urls')),
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

