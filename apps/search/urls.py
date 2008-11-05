# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.search`` application.

search_results
--------------

Displays search results.

- Named URL   : ``search_results``
- View        : ``critica.apps.search.views.results``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^results/$', 
        'critica.apps.search.views.results', 
        name='search_results',
    ),
)

