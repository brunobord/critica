# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.pages`` application.

"""
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from critica.apps.front.views import _get_current_issue
from critica.apps.pages.models import Page


def page_legal(request):
    """
    Displays the legal page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    context['page'] = get_object_or_404(Page.objects.all(), slug='mentions-legales', is_published=True)
    
    return render_to_response(
        'pages/page.html', 
        context, 
        context_instance=RequestContext(request))


def page_ads(request):
    """
    Displays the ad page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    context['page'] = get_object_or_404(Page.objects.all(), slug='publicites', is_published=True)
    
    return render_to_response(
        'pages/page.html', 
        context, 
        context_instance=RequestContext(request))


