# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.polls`` application.

"""
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.polls.models import Poll


register = template.Library()


@register.inclusion_tag('polls/form.html', takes_context=True)
def display_poll(context):
    """
    Displays the poll form.
    
    """
    # Gets current issue
    issue = context['current_issue']
    
    # Gets request object for REMOTE_ADDR
    request = context['request']
    
    # Gets the poll related to the current issue, otherwise None.
    try:
        poll = Poll.published.filter(issues__id=issue.id)
        poll = poll.order_by('-creation_date')
        poll = poll[0:1].get()
    except ObjectDoesNotExist:
        poll = None
         
    return {
        'poll': poll,
        'MEDIA_URL': context['MEDIA_URL'],
        'REMOTE_ADDR': request.META.get('REMOTE_ADDR')
    }

