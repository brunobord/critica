# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.pages`` application.

pages_page
----------

Displays a given page (based on its slug).

- Named URL   : ``pages_page``
- View        : ``critica.apps.pages.views.page``
- Arguments   : page slug

pages_index
-----------

Displays page list.

- Named URL   : ``pages_index``
- View        : ``critica.apps.pages.views.index``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<page_slug>[-\w]+)/$', 
        'critica.apps.pages.views.page', 
        name='pages_page',
    ),
    url(r'^$', 
        'critica.apps.pages.views.index', 
        name='pages_index',
    ),
)

