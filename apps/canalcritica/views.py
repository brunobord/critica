# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.canalcritica`` application.

"""
from django.views.generic.simple import direct_to_template
from critica.apps.issues.views import _get_current_issue

def index(request):
    """
    View of canalcritica page.
    
    """
    context = {}
    context['issue'] = _get_current_issue
    context['is_current'] = True
    return direct_to_template(request, 'canalcritica/index.html', context)
