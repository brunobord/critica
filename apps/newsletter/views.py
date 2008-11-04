# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.newsletter`` application.

"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from critica.apps.newsletter.models import Subscriber
from critica.apps.newsletter.forms import SubscriberForm
from critica.apps.issues.views import _get_current_issue


def newsletter(request):
    """
    View of newsletter form.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('newsletter_thanks'))
    else:
        form = SubscriberForm(auto_id=True)
        
    context['form'] = form

    return direct_to_template(request, 'newsletter/form_page.html', context)


def newsletter_thanks(request):
    """
    View of newsletter thanks message.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    
    return direct_to_template(request, 'newsletter/thanks.html', context)
