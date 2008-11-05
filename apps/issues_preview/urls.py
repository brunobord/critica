# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.issues_preview`` application.

issues_preview_category_anger
------------------

Displays issue preview of anger category.

- Named URL   : ``issues_preview_category_anger``
- View        : ``critica.apps.issues_preview.views.preview_category_anger``
- Arguments   : None

issues_preview_category_epicurien
---------------------------------

Displays issue preview of epicurien category.

- Named URL   : ``issues_preview_category_epicurien``
- View        : ``critica.apps.issues_preview.views.preview_category_epicurien``
- Arguments   : None

issues_preview_category_voyages
-------------------------------

Displays issue preview of voyages category.

- Named URL   : ``issues_preview_category_voyages``
- View        : ``critica.apps.issues_preview.views.preview_category_voyages``
- Arguments   : None

issues_preview_category_regions
-------------------------------

Displays issue preview of regions category.

- Named URL   : ``issues_preview_category_regions``
- View        : ``critica.apps.issues_preview.views.preview_category_regions``
- Arguments   : None

issues_preview_category
-----------------------

Displays issue preview of a given category (based on its slug).

- Named URL   : ``issues_preview_category``
- View        : ``critica.apps.issues_preview.views.preview_category``
- Arguments   : category slug

issues_preview_home
-------------------

Displays issue preview of homepage.

- Named URL   : ``issues_preview_home``
- View        : ``critica.apps.issues_preview.views.preview_home``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<issue_key>[-\w]+)/coup-de-gueule/$', 
        'critica.apps.issues_preview.views.preview_category_anger', 
        name='issues_preview_category_anger',
    ),
    url(r'^(?P<issue_key>[-\w]+)/epicurien/$', 
        'critica.apps.issues_preview.views.preview_category_epicurien', 
        name='issues_preview_category_epicurien',
    ),
    url(r'^(?P<issue_key>[-\w]+)/voyages/$', 
        'critica.apps.issues_preview.views.preview_category_voyages', 
        name='issues_preview_category_voyages',
    ),
    url(r'^(?P<issue_key>[-\w]+)/regions/$', 
        'critica.apps.issues_preview.views.preview_category_regions', 
        name='issues_preview_category_regions',
    ),
    url(r'^(?P<issue_key>[-\w]+)/(?P<category_slug>[-\w]+)/$', 
        'critica.apps.issues_preview.views.preview_category', 
        name='issues_preview_category',
    ),
    url(r'^(?P<issue_key>[-\w]+)/$', 
        'critica.apps.issues_preview.views.preview_home', 
        name='issues_preview_home',
    ),
)

