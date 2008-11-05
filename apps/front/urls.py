# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.front`` application.

category_anger
--------------

Displays current issue anger category.

- Named URL   : ``category_anger``
- View        : ``critica.apps.front.views.category_anger``
- Arguments   : None

category_epicurien
------------------

Displays current issue epicurien category.

- Named URL   : ``category_epicurien``
- View        : ``critica.apps.front.views.category_epicurien``
- Arguments   : None

category_voyages
----------------

Displays current issue voyages category.

- Named URL   : ``category_voyages``
- View        : ``critica.apps.front.views.category_voyages``
- Arguments   : None

category_regions
----------------

Displays current issue regions category.

- Named URL   : ``issues_archive_category_regions``
- View        : ``critica.apps.front.views.category_regions``
- Arguments   : None

category
--------

Displays current issue given category (based on its slug).

- Named URL   : ``category``
- View        : ``critica.apps.front.views.archive_category``
- Arguments   : category slug

home
----

Displays current issue homepage.

- Named URL   : ``home``
- View        : ``critica.apps.front.views.home``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^coup-de-gueule/$', 
        'critica.apps.front.views.anger', 
        name='category_anger',
    ),
    url(r'^epicurien/$', 
        'critica.apps.front.views.epicurien', 
        name='category_epicurien',
    ),
    url(r'^voyages/$', 
        'critica.apps.front.views.voyages', 
        name='category_voyages',
    ),
    url(r'^regions/$', 
        'critica.apps.front.views.regions', 
        name='category_regions',
    ),
    url(r'^(?P<category_slug>[-\w]+)/$', 
        'critica.apps.front.views.category', 
        name='category',
    ),
    url(r'^$', 
        'critica.apps.front.views.home', 
        name='home',
    ),
)


