# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.partnerlinks`` application.

"""
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.partnerlinks.models import PartnerLink


register = template.Library()


@register.inclusion_tag('partnerlinks/links.html', takes_context=True)
def display_partnerlinks(context):
    """
    Displays active partner links.
    
    """
    partnerlinks = PartnerLink.objects.filter(is_active=True)
    return {
        'partnerlinks': partnerlinks,
    }
