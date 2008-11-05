# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.polls`` application.

polls_poll_vote
---------------

POST request to post a vote.

- Named URL   : ``polls_poll_vote``
- View        : ``critica.apps.polls.views.poll_vote``
- Arguments   : None

polls_poll_results
------------------

Displays poll vote results.

- Named URL   : ``polls_poll_results``
- View        : ``critica.apps.polls.views.poll_results``
- Arguments   : poll slug

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url('^vote/$', 
        'critica.apps.polls.views.poll_vote', 
        name='polls_poll_vote',
    ),
    url('^(?P<poll_slug>[-\w]+)/$', 
        'critica.apps.polls.views.poll_results', 
        name='polls_poll_results',
    ),
)

