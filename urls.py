# -*- coding: utf-8 -*-
"""
URLs of ``critica`` project.

"""
import os.path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from critica.apps.custom_admin.sites import custom_site
from critica.apps.custom_admin.views import dashboard
from critica.apps.syndication.feeds import LatestRss
from critica.apps.syndication.feeds import LatestByCategoryRss


# Admin
# ------------------------------------------------------------------------------
admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/dashboard/(?P<issue>\d+)/$', dashboard),
    (r'^admin/dashboard/$', dashboard),
    (r'^admin/(.*)', custom_site.root),
    (r'^django-admin/(.*)', admin.site.root),
)

# Pages
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^publicites/$', 'critica.apps.pages.views.page_ads', name='page_ads'),
    url(r'^mentions-legales/$', 'critica.apps.pages.views.page_legal', name='page_legal'),
)

# Syndication
# ------------------------------------------------------------------------------
feeds = {
    'articles': LatestRss,
    'rubriques': LatestByCategoryRss,
}

urlpatterns += patterns('',
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^rss/$', 'critica.apps.syndication.views.rss_index', name='rss'),
)

# Polls
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url('^sondage/vote/$', 'critica.apps.polls.views.poll_vote', name='poll_vote'),
    url('^sondage/(?P<poll_slug>[-\w]+)/$', 'critica.apps.polls.views.poll_results', name='poll_results'),
)

# Newsletter
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url('^newsletter/$', 'critica.apps.newsletter.views.newsletter', name='newsletter'),
    url('^newsletter/merci/$', 'critica.apps.newsletter.views.newsletter_thanks', name='newsletter_thanks'),
)

# Send to a friend
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url('^envoyer/$', 'critica.apps.sendfriend.views.sendfriend', name="sendfriend"),
    url('^envoyer/merci/$', 'critica.apps.sendfriend.views.sendfriend_thanks', name="sendfriend_thanks"),
)

# Search
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^search/results/$', 'critica.apps.search.views.search', name='search'),
)

# Tags
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^tags/(?P<tag>[-\w]+)/$', 'critica.apps.tags.views.tag', name='tag'),
    url(r'^tags/$', 'critica.apps.tags.views.tags', name='tags'),
)

# Archives
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^archives/(?P<issue_number>\d+)/coup-de-gueule/$', 'critica.apps.archives.views.issuearchive_anger', name='issuearchive_category_anger'),
    url(r'^archives/(?P<issue_number>\d+)/epicurien/$', 'critica.apps.archives.views.issuearchive_epicurien', name='issuearchive_category_epicurien'),
    url(r'^archives/(?P<issue_number>\d+)/voyages/$', 'critica.apps.archives.views.issuearchive_voyages', name='issuearchive_category_voyages'),
    url(r'^archives/(?P<issue_number>\d+)/regions/$', 'critica.apps.archives.views.issuearchive_regions', name='issuearchive_category_regions'),
    url(r'^archives/(?P<issue_number>\d+)/(?P<category_slug>[-\w]+)/$', 'critica.apps.archives.views.issuearchive_category', name='issuearchive_category'),
    url(r'^archives/(?P<issue_number>\d+)/$', 'critica.apps.archives.views.issuearchive_home', name='issuearchive_home'),
    url(r'^archives/$', 'critica.apps.archives.views.archives', name='archives'),
)

# Issue preview
# ------------------------------------------------------------------------------
urlpatterns += patterns('',
    url(r'^preview/(?P<issue_key>[-\w]+)/coup-de-gueule/$', 'critica.apps.issuepreview.views.issuepreview_anger', name='issuepreview_category_anger'),
    url(r'^preview/(?P<issue_key>[-\w]+)/epicurien/$', 'critica.apps.issuepreview.views.issuepreview_epicurien', name='issuepreview_category_epicurien'),
    url(r'^preview/(?P<issue_key>[-\w]+)/voyages/$', 'critica.apps.issuepreview.views.issuepreview_voyages', name='issuepreview_category_voyages'),
    url(r'^preview/(?P<issue_key>[-\w]+)/regions/$', 'critica.apps.issuepreview.views.issuepreview_regions', name='issuepreview_category_regions'),
    url(r'^preview/(?P<issue_key>[-\w]+)/(?P<category_slug>[-\w]+)/$', 'critica.apps.issuepreview.views.issuepreview_category', name='issuepreview_category'),
    url(r'^preview/(?P<issue_key>[-\w]+)/$', 'critica.apps.issuepreview.views.issuepreview_home', name='issuepreview_home'),
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

