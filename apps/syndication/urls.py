# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.syndication`` application.

syndication_index
-----------------

Displays feed list.

- Named URL   : ``syndication_index``
- View        : ``critica.apps.syndication.views.index``
- Arguments   : None

"""
from django.conf.urls.defaults import *
from critica.apps.syndication.feeds import LatestRss
from critica.apps.syndication.feeds import LatestByCategoryRss


feeds = {
    'articles': LatestRss,
    'rubriques': LatestByCategoryRss,
}

# Feeds
urlpatterns = patterns('',
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

# Index page
urlpatterns += patterns('',
    url(r'^$', 
        'critica.apps.syndication.views.index', 
        name='syndication_index',
    ),
)
