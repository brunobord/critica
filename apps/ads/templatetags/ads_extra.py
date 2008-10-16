# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.ads.models import Ad
from critica.apps.ads.models import AdBanner


register = template.Library()


@register.inclusion_tag('front/includes/ad.html')
def display_ad(format, page, location):
    width, height = format.split('x')
    try:
        banner = AdBanner.objects.get(
            ads__format__width=width, 
            ads__format__height=height,
            ads__page__slug=page, 
            ads__location__position=location
        )
    except ObjectDoesNotExist:
        banner = None
    return {
        'banner': banner,
        'format': format,
        'format_width': width,
        'format_height': height,
    }

