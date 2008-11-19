# -*- coding: utf-8 -*-
"""
URLs of ``critica`` project.

"""
import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from critica.apps.custom_admin.sites import custom_site


# Admin
# ------------------------------------------------------------------------------
admin.autodiscover()

# Custom views
urlpatterns = patterns('',
    (r'^admin/newsletter/preview/(?P<issue_number>\d+)/(?P<format>[-\w]+)/', 'critica.apps.newsletter.views.admin_preview'),
    (r'^admin/ads_dashboard/',      include('critica.apps.ads_dashboard.urls')),
    (r'^admin/issues_dashboard/',   include('critica.apps.issues_dashboard.urls')),
)

# Admin sites
urlpatterns += patterns('',
    (r'^admin/(.*)',        custom_site.root),
    (r'^django-admin/(.*)', admin.site.root),
)

# Applications
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    (r'^rss/',          include('critica.apps.syndication.urls')),
    (r'^newsletter/',   include('critica.apps.newsletter.urls')),
    (r'^envoyer/',      include('critica.apps.sendfriend.urls')),
    (r'^sondages/',     include('critica.apps.polls.urls')),
    (r'^tags/',         include('critica.apps.tags.urls')),
    (r'^recherche/',    include('critica.apps.search.urls')),
    (r'^archives/',     include('critica.apps.issues_archive.urls')),
    (r'^preview/',      include('critica.apps.issues_preview.urls')),
    (r'^ads_preview/',  include('critica.apps.ads_preview.urls')),
    (r'^pages/',        include('critica.apps.pages.urls')),
    (r'^canalcritica/', include('critica.apps.canalcritica.urls')),
    (r'',               include('critica.apps.front.urls')),
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

