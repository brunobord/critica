# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.partner_links`` application.

"""
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.partner_links.models import PartnerLink


register = template.Library()


@register.inclusion_tag('partner_links/links.html', takes_context=True)
def display_partner_links(context):
    """
    Displays active partner links.
    
    """
    partner_links = PartnerLink.objects.filter(is_active=True)
    return {
        'partner_links': partner_links,
    }
