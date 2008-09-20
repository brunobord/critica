"""
URLs for ``critica.apps.syndication``::
    
    rss
        Introduces RSS and lists feeds.
        Sample URL: /rss/
        Takes no arguments.
        
"""
from django.conf.urls.defaults import *
from critica.apps.syndication.feeds import LatestArticles
from critica.apps.syndication.feeds import LatestArticlesByCategory
from critica.apps.categories.models import Category


# Feeds
# ------------------------------------------------------------------------------
feeds = {
    'articles': LatestArticles,
    'rubriques': LatestArticlesByCategory,
}

urlpatterns = patterns('',
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

# Index
# ------------------------------------------------------------------------------
urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 
        'direct_to_template', 
        {
            'template': 'syndication/index.html',
            'extra_context': {
                'categories': Category.objects.all(),
            }
        },
        name='rss'
    ),
)
