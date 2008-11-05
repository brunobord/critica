# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.sendfriend`` application.

sendfriend_thanks
-----------------

Displays the thanks message after sending.

- Named URL   : ``sendfriend_thanks``
- View        : ``critica.apps.sendfriend.views.thanks``
- Arguments   : None

sendfriend_index
----------------

Displays sendfriend form.

- Named URL   : ``sendfriend_index``
- View        : ``critica.apps.sendfriend.views.index``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url('^ok/$', 
        'critica.apps.sendfriend.views.thanks', 
        name='sendfriend_thanks',
    ),
    url('^$', 
        'critica.apps.sendfriend.views.index', 
        name='sendfriend_index',
    ),
)

