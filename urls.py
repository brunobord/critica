# -*- coding: utf-8 -*-
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

# Issue preview
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^preview/(?P<issue_key>[-\w]+)/coup-de-gueule/$', 'critica.apps.front.views.issuepreview_anger', name='issuepreview_category_anger'),
    url(r'^preview/(?P<issue_key>[-\w]+)/epicurien/$', 'critica.apps.front.views.issuepreview_epicurien', name='issuepreview_category_epicurien'),
    url(r'^preview/(?P<issue_key>[-\w]+)/voyages/$', 'critica.apps.front.views.issuepreview_voyages', name='issuepreview_category_voyages'),
    url(r'^preview/(?P<issue_key>[-\w]+)/regions/$', 'critica.apps.front.views.issuepreview_regions', name='issuepreview_category_regions'),
    url(r'^preview/(?P<issue_key>[-\w]+)/(?P<category_slug>[-\w]+)/$', 'critica.apps.front.views.issuepreview_category', name='issuepreview_category'),
    url(r'^preview/(?P<issue_key>[-\w]+)/$', 'critica.apps.front.views.issuepreview_home', name='issuepreview_home'),
)

# Home and categories
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^coup-de-gueule/$', 'critica.apps.front.views.anger', name='category_anger'),
    url(r'^epicurien/$', 'critica.apps.front.views.epicurien', name='category_epicurien'),
    url(r'^voyages/$', 'critica.apps.front.views.voyages', name='category_voyages'),
    url(r'^regions/$', 'critica.apps.front.views.regions', name='category_regions'),
    url(r'^(?P<category_slug>[-\w]+)/$', 'critica.apps.front.views.category', name='category'),
    url(r'^$', 'critica.apps.front.views.home', name='home'),
)

#urlpatterns += patterns('',
    #(r'^archives/', include('critica.apps.archives.urls')),
    #(r'^pages/', include('critica.apps.pages.urls')),
    #(r'^rss/', include('critica.apps.syndication.urls')),
    #(r'', include('critica.apps.categories.urls')),
#)

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

