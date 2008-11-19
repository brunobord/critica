# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.tags`` application.

tags_index
----------

Displays the tags index page (tag cloud).

- Named URL   : ``tags_index``
- View        : ``critica.apps.tags.views.index``
- Arguments   : None

tags_tag
--------

Displays object tagged with a given tag.

- Named URL   : ``tags_tag``
- View        : ``critica.apps.tags.views.tag``
- Arguments   : tag name

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<tag>[^/]+)/$', 
        'critica.apps.tags.views.tag', 
        name='tags_tag',
    ),
    url(r'^$', 
        'critica.apps.tags.views.index', 
        name='tags_index',
    ),
)
