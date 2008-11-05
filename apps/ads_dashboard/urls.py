# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.ads_dashboard`` application.

ads_dasboard_index
------------------

Displays the dashboard for the latest ad campaign. Displays links of available
campaigns too.

- Named URL   : ``ads_dashboard_index``
- View        : ``critica.apps.ads_dashboard.views.index``
- Arguments   : None

ads_dashboard_campaign
----------------------

Displays the dashboard of a given campaign (based on its id).

- Named URL   : ``ads_dashboard_campaign``
- View        : ``critica.apps.ads_dashboard.views.index``
- Arguments   : campaign id

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<campaign>\d+)/$', 
        'critica.apps.ads_dashboard.views.index', 
        name='ads_dashboard_campaign',
    ),
    url(r'^$', 
        'critica.apps.ads_dashboard.views.index', 
        name='ads_dashboard_index',
    ),
)
