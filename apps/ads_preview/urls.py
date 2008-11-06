# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.ads_preview`` application.

ads_preview_category_anger
------------------

Displays ads preview on anger category.

- Named URL   : ``ads_preview_category_anger``
- View        : ``critica.apps.ads_preview.views.preview_category_anger``
- Arguments   : campaign id

ads_preview_category_epicurien
---------------------------------

Displays ads preview on epicurien category.

- Named URL   : ``ads_preview_category_epicurien``
- View        : ``critica.apps.ads_preview.views.preview_category_epicurien``
- Arguments   : campaign id

ads_preview_category_voyages
-------------------------------

Displays ads preview on voyages category.

- Named URL   : ``ads_preview_category_voyages``
- View        : ``critica.apps.ads_preview.views.preview_category_voyages``
- Arguments   : campaign id

ads_preview_category_regions
-------------------------------

Displays ads preview on regions category.

- Named URL   : ``ads_preview_category_regions``
- View        : ``critica.apps.ads_preview.views.preview_category_regions``
- Arguments   : campaign id

ads_preview_category
-----------------------

Displays ads preview on a given category.

- Named URL   : ``ads_preview_category``
- View        : ``critica.apps.ads_preview.views.preview_category``
- Arguments   : campaign id, category slug

ads_preview_home
-------------------

Displays ads preview on the homepage.

- Named URL   : ``ads_preview_home``
- View        : ``critica.apps.ads_preview.views.preview_home``
- Arguments   : campaign id

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<campaign_id>\d+)/coup-de-gueule/$', 
        'critica.apps.ads_preview.views.preview_category_anger', 
        name='ads_preview_category_anger',
    ),
    url(r'^(?P<campaign_id>\d+)/epicurien/$', 
        'critica.apps.ads_preview.views.preview_category_epicurien', 
        name='ads_preview_category_epicurien',
    ),
    url(r'^(?P<campaign_id>\d+)/voyages/$', 
        'critica.apps.ads_preview.views.preview_category_voyages', 
        name='ads_preview_category_voyages',
    ),
    url(r'^(?P<campaign_id>\d+)/regions/$', 
        'critica.apps.ads_preview.views.preview_category_regions', 
        name='ads_preview_category_regions',
    ),
    url(r'^(?P<campaign_id>\d+)/(?P<category_slug>[-\w]+)/$', 
        'critica.apps.ads_preview.views.preview_category', 
        name='ads_preview_category',
    ),
    url(r'^(?P<campaign_id>\d+)/$', 
        'critica.apps.ads_preview.views.preview_home', 
        name='ads_preview_home',
    ),
)

