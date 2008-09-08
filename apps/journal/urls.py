"""
URLs for ``critica.apps.journal``::
        
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
    url(r'^(?P<category>[\w-]+)/$',
        category,
        name='category'
    ),
    url(r'^$',
        home,
        name='home',
    ),
)

