"""
URLs for ``critica.apps.journal``::

    archives_issue_category
        Journal archives for a given issue and a given category.
        Sample URL: /archives/124/national/
        Takes two arguments: issue number and category slug.
        
    archives_issue
        Journal archives for a given issue.
        Sample URL: /archives/124/
        Takes one argument: issue number.
        
    archives
        Journal archives.
        Sample URL: /archives/
        Takes no arguments.
        
    category
        Journal current issue category.
        Sample URL: /sports/
        Takes one argument: category slug.
        
    home
        Journal's cover (homepage).
        Sample URL: /
        Takes no arguments.
        
"""
from django.conf.urls.defaults import *
from critica.apps.journal.views import home
from critica.apps.journal.views import category
from critica.apps.journal.views import archives
from critica.apps.journal.views import archives_issue
from critica.apps.journal.views import archives_issue_category


urlpatterns = patterns('',
    url(r'^archives/(?P<issue>\d+)/(?P<category>[-\w]+)/$',
        archives_issue_category,
        name='archives_issue_category',
    ),
    url(r'^archives/(?P<issue>\d+)/$',
        archives_issue,
        name='archives_issue',
    ),
    url(r'^archives/$',
        archives,
        name='archives',
    ),
    url(r'^(?P<category>[-\w]+)/$',
        category,
        name='category'
    ),
    url(r'^$',
        home,
        name='home',
    ),
)

