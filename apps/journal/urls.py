"""
URLs for ``critica.apps.journal``::
    
    archives_article
        Journal archived article detail.
        Sample URL: /archives/2008/09/08/this-is-an-archived-article/
        Takes four arguments: year, month, day and article slug.
        
    archives_day
        Journal archives for a given day.
        Sample URL: /archives/2008/09/08/
        Takes three arguments: year, month and day.
        
    archives_month
        Journal archives for a given month.
        Sample URL: /archives/2008/09/
        Takes two arguments: year and month.
        
    archives_year
        Journal archives for a given year.
        Sample URL: /archives/2008/
        Takes one argument: year.
        
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
from critica.apps.journal.models import Issue, Page, Article


# Archives
# ------------------------------------------------------------------------------
archives_dict = {
    'queryset': Issue.complete.all(), 
    'date_field': 'publication_date',
}

urlpatterns = patterns('django.views.generic.date_based',
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
        'object_detail',
        dict(
            queryset=Article.complete.all(),
            date_field='publication_date',
            month_format='%m',
            slug_field='slug',
        ),
        name='archives_article',
    ),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 
        'archive_day', 
        dict(
            queryset=Article.complete.order_by('category'),
            date_field='publication_date',
            template_name='journal/issue_archive_day.html',
            month_format='%m',
        ), 
        name='archives_day',
    ),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$', 
        'archive_month', 
        dict(
            queryset=Issue.complete.all(),
            date_field='publication_date',
            month_format='%m'
        ), 
        name='archives_month',
    ),
    url(r'^archives/(?P<year>\d{4})/$', 
        'archive_year', 
        dict(
            queryset=Issue.complete.all(),
            date_field='publication_date',
            make_object_list=True,
        ), 
        name='archives_year',
    ),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^archives/$', 
        'direct_to_template', 
        {'template': 'journal/issue_archive.html', 'extra_context': {'issues': Issue.complete.all()}}, 
        name='archives',
    ),
)

# Category
# ------------------------------------------------------------------------------
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^(?P<slug>[-\w]+)/$',
        'object_detail',
        dict(
            queryset = Page.complete.all(),
            slug_field = 'category__slug',
            template_name = 'journal/category.html',
        ),
        name='category',
    ),
)

# Homepage
# ------------------------------------------------------------------------------
urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 
        'direct_to_template', 
        {
            'template': 'journal/home.html',
            'extra_context': {
                'page': Page.complete.get(category__pk=1),
            },
        },
        name='home'
    ),
)

