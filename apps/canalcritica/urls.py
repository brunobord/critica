# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.canalcritica`` application.

canalcritica_index
------------------

Displays canalcritica page.

- Named URL   : ``canalcritica_index``
- View        : ``critica.apps.canalcritica.views.index``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 
        'critica.apps.canalcritica.views.index', 
        name='canalcritica_index',
    ),
)

