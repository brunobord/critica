# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.newsletter`` application.

newsletter_ok
-------------

Displays the thanks message after registering.

- Named URL   : ``newsletter_thanks``
- View        : ``critica.apps.newsletter.views.thanks``
- Arguments   : None

newsletter_index
----------------

Displays newsletter form.

- Named URL   : ``newsletter_index``
- View        : ``critica.apps.newsletter.views.index``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url('^ok/$', 
        'critica.apps.newsletter.views.thanks', 
        name='newsletter_thanks',
    ),
    url('^$', 
        'critica.apps.newsletter.views.index', 
        name='newsletter_index',
    ),
)

