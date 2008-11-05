# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.issues_archive`` application.

issues_archive_category_anger
-----------------------------

Displays issue archive of anger category.

- Named URL   : ``issues_archive_category_anger``
- View        : ``critica.apps.issues_archive.views.archive_category_anger``
- Arguments   : None

issues_archive_category_epicurien
---------------------------------

Displays issue archive of epicurien category.

- Named URL   : ``issues_archive_category_epicurien``
- View        : ``critica.apps.issues_archive.views.archive_category_epicurien``
- Arguments   : None

issues_archive_category_voyages
-------------------------------

Displays issue archive of voyages category.

- Named URL   : ``issues_archive_category_voyages``
- View        : ``critica.apps.issues_archive.views.archive_category_voyages``
- Arguments   : None

issues_archive_category_regions
-------------------------------

Displays issue archive of regions category.

- Named URL   : ``issues_archive_category_regions``
- View        : ``critica.apps.issues_archive.views.archive_category_regions``
- Arguments   : None

issues_archive_category
-----------------------

Displays issue archive of a given category (based on its slug).

- Named URL   : ``issues_archive_category``
- View        : ``critica.apps.issues_archive.views.archive_category``
- Arguments   : category slug

issues_archive_home
-------------------

Displays issue archive of homepage.

- Named URL   : ``issues_archive_home``
- View        : ``critica.apps.issues_archive.views.archive_home``
- Arguments   : None

issues_archive_index
--------------------

Displays issue archive index page (archive list).

- Named URL   : ``issues_archive_index``
- View        : ``critica.apps.issues_archive.views.index``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(?P<issue_number>\d+)/coup-de-gueule/$', 
        'critica.apps.issues_archive.views.archive_category_anger', 
        name='issues_archive_category_anger',
    ),
    url(r'^(?P<issue_number>\d+)/epicurien/$', 
        'critica.apps.issues_archive.views.archive_category_epicurien', 
        name='issues_archive_category_epicurien',
    ),
    url(r'^(?P<issue_number>\d+)/voyages/$', 
        'critica.apps.issues_archive.views.archive_category_voyages', 
        name='issues_archive_category_voyages',
    ),
    url(r'^(?P<issue_number>\d+)/regions/$', 
        'critica.apps.issues_archive.views.archive_category_regions', 
        name='issues_archive_category_regions',
    ),
    url(r'^(?P<issue_number>\d+)/(?P<category_slug>[-\w]+)/$', 
        'critica.apps.issues_archive.views.archive_category', 
        name='issues_archive_category',
    ),
    url(r'^(?P<issue_number>\d+)/$', 
        'critica.apps.issues_archive.views.archive_home', 
        name='issues_archive_home',
    ),
    url(r'^$', 
        'critica.apps.issues_archive.views.index',
        name='issues_archive_index',
    ),
)


