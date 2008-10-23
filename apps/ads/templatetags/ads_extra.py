# -*- coding: utf-8 -*-
import datetime
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdDefaultBanner
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarousel


register = template.Library()


@register.inclusion_tag('front/includes/ad.html')
def display_ad(format, page, location):
    width, height = format.split('x')
    today = datetime.date.today()
    try:
        banner = AdBanner.objects.get(
            positions__format__width=width, 
            positions__format__height=height,
            positions__page__slug=page, 
            positions__location__position=location,
            starting_date__lte=today,
            ending_date__gte=today,
        )
    except ObjectDoesNotExist:
        banner = None

    try:
        default_banner = AdDefaultBanner.objects.get(
            positions__format__width=width, 
            positions__format__height=height,
            positions__page__slug=page, 
            positions__location__position=location
        )
    except ObjectDoesNotExist:
        default_banner = None
        
    return {
        'banner': banner,
        'default_banner': default_banner,
        'format': format,
        'format_width': width,
        'format_height': height,
    }


@register.inclusion_tag('front/includes/carousel.html')
def display_carousel(format, page, location):
    width, height = format.split('x')
    today = datetime.date.today()
    try:
        carousel = AdCarousel.objects.get(
            positions__format__width=width, 
            positions__format__height=height,
            positions__page__slug=page, 
            positions__location__position=location,
            starting_date__lte=today,
            ending_date__gte=today,
        )
    except ObjectDoesNotExist:
        carousel = None

    return {
        'carousel': carousel,
        'format': format,
        'format_width': width,
        'format_height': height,
    }
    

