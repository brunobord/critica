# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.newsletter`` application.

"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.simple import direct_to_template
from critica.apps.newsletter.models import Subscriber
from critica.apps.newsletter.forms import SubscriberForm
from critica.apps.newsletter.forms import UnsubscribeForm
from critica.apps.issues.views import _get_current_issue


def subscribe_form(request):
    """
    View of newsletter subscribing form.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('newsletter_subscribe_thanks'))
    else:
        form = SubscriberForm(auto_id=True)
        
    context['form'] = form
    return direct_to_template(request, 'newsletter/subscribe_form.html', context)


def subscribe_thanks(request):
    """
    View of newsletter subscribing thanks message.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    return direct_to_template(request, 'newsletter/subscribe_thanks.html', context)
    

def unsubscribe_form(request):
    """
    View of newsletter unsubscribing form.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            subscriber = Subscriber.objects.get(email=form.cleaned_data['email'])
            subscriber.delete()
            return HttpResponseRedirect(reverse('newsletter_unsubscribe_thanks'))
    else:
        form = UnsubscribeForm(auto_id=True)
    context['form'] = form
    return direct_to_template(request, 'newsletter/unsubscribe_form.html', context)
    
    
def unsubscribe_thanks(request):
    """
    View of newsletter unsubscribe thanks message.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    return direct_to_template(request, 'newsletter/unsubscribe_thanks.html', context)


