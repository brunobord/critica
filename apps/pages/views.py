# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.pages`` application.

"""
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.front.views import _get_current_issue
from critica.apps.pages.models import Page


def index(request):
    """
    View of page list.
    
    """
    context = {}
    try:
        context['pages'] = Page.objects.filter(is_published=True).order_by('name')
    except ObjectDoesNotExist:
        context['pages'] = None
    return direct_to_template(request, 'pages/index.html', context)


def page(request, page_slug):
    """
    View of a page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    context['page'] = get_object_or_404(Page.objects.all(), slug=page_slug, is_published=True)
    return direct_to_template(request, 'pages/page.html', context)


