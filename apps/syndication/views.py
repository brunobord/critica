# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.syndication`` application.

"""
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.front.views import _get_current_issue
from critica.apps.categories.models import Category


def index(request):
    """
    View of RSS feed list.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    try:
        context['categories'] = Category.objects.all()
    except ObjectDoesNotExist:
        context['categories'] = False
    return direct_to_template(request, 'syndication/index.html', context)
