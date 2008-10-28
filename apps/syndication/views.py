# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.syndication`` application.

"""
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from critica.apps.front.views import _get_current_issue
from critica.apps.categories.models import Category


def rss_index(request):
    """
    Displays RSS index page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    try:
        context['categories'] = Category.objects.all()
    except ObjectDoesNotExist:
        context['categories'] = False
        
    return render_to_response(
        'syndication/rss_index.html', 
        context, 
        context_instance=RequestContext(request))
