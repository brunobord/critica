# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.issues_dashboard`` application.

issues_dashboard_index
----------------------

Displays the dashboard for the issue of the day. Displays links of other issues too.

- Named URL   : ``issues_dashboard_index``
- View        : ``critica.apps.issues_dashboard.views.index``
- Arguments   : None

issues_dashboard_issue
----------------------

Displays the dashboard of a given issue (based on its id).

- Named URL   : ``issues_dashboard_issue``
- View        : ``critica.apps.issues_dashboard.views.index``
- Arguments   : issue id

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<issue>\d+)/$', 
        'critica.apps.issues_dashboard.views.index', 
        name='issues_dashboard_issue',
    ),
    url(r'^$', 
        'critica.apps.issues_dashboard.views.index',
        name='issues_dashboard_index',
    ),
)
