"""
URLs for ``critica.apps.journal``::

    archives_issue_article
        Journal issue's article detail.
        Sample URL: /archives/114/sports/aviron-bayonnais/
        Takes three arguments: issue number, category slug and article slug.
        
    archives_issue_category
        Journal issue's category.
        Sample URL: /archives/114/sports/
        Takes two arguments: issue number and category slug.
        
    archives_issue
        Journal issue.
        Sample URL: /archives/114/
        Takes one argument: issue number.
        
    archives
        Journal issue archives.
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
from critica.apps.journal.views import home, category
from critica.apps.journal.views import archives, archives_issue
from critica.apps.journal.views import archives_issue_category, archives_issue_article


urlpatterns = patterns('',
    url(r'^archives/(?P<issue>\d+)/(?P<category>[\w-]+)/(?P<article>[\w-]+)/$',
        archives_issue_article,
        name='archives_issue_article',
    ),
    url(r'^archives/(?P<issue>\d+)/(?P<category>[\w-]+)/$',
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
    url(r'^(?P<category>[\w-]+)/$',
        category,
        name='category'
    ),
    url(r'^$',
        home,
        name='home',
    ),
)

