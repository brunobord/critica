# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.issues_preview`` application.

"""
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.issues.models import Issue


register = template.Library()

@register.inclusion_tag('issues_preview/includes/switcher.html', takes_context=True)
def display_issues_preview_switcher(context):
    """
    Displays issues preview switcher.
    
    """
    request = context['request']
    try:
        issues = Issue.objects.filter(is_published=False).order_by('-number')[:20]
    except ObjectDoesNotExist:
        issues = None
    return {
        'request': request,
        'issues': issues,
    }

