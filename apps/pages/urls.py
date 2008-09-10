"""
URLs for ``critica.apps.pages``::

    pages_page
        Page detail
        Sample URL: /pages/legal/
        View: page_detail
        Takes one argument: slug

"""
from django.conf.urls.defaults import *
from critica.apps.pages.models import Page


urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^(?P<slug>[-\w]+)/$', 
        'object_detail',
        dict(
            queryset=Page.published.all(),
            template_name='pages/page_detail.html',
        ),
        name='pages_page',
    )
)

