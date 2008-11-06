# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.ads_preview`` application.

"""
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.ads.models import AdCampaign


register = template.Library()

@register.inclusion_tag('ads_preview/includes/switcher.html', takes_context=True)
def display_ads_preview_switcher(context):
    """
    Displays ads preview switcher.
    
    """
    request = context['request']
    try:
        campaigns = AdCampaign.objects.order_by('name')[:20]
    except ObjectDoesNotExist:
        campaigns = None
    return {
        'request': request,
        'campaigns': campaigns,
    }

