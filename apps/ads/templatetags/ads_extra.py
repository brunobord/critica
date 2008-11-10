# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.ads`` application.

"""
import datetime
from decimal import getcontext
from decimal import Decimal
from decimal import ROUND_HALF_EVEN
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdDefaultBanner
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarousel


register = template.Library()

@register.inclusion_tag('front/includes/ad.html', takes_context=True)
def display_ad(context, format, page, location):
    """
    Displays an ad related to its format, its page and its location.
    
    """
    # Gets campaign if it exists
    if context.has_key('campaign'):
        campaign = context['campaign']
    else:
        campaign = None
    
    # Gets width and height
    width, height = format.split('x')
    
    # Gets banner
    try:
        banner = AdBanner.objects.filter(
            positions__format__width=width, 
            positions__format__height=height,
            positions__page__slug=page, 
            positions__location__position=location)
        if campaign:
            banner = banner.filter(campaign=campaign)[0:1].get()
        else: 
            banner = banner.filter(starting_date__lte=datetime.date.today(), ending_date__gte=datetime.date.today())[0:1].get()
    except ObjectDoesNotExist:
        banner = None
    
    # Gets default banner
    try:
        default_banner = AdDefaultBanner.objects.get(
            positions__format__width=width, 
            positions__format__height=height,
            positions__page__slug=page, 
            positions__location__position=location)
    except ObjectDoesNotExist:
        default_banner = None
        
    return {
        'MEDIA_URL': context['MEDIA_URL'],
        'banner': banner,
        'default_banner': default_banner,
        'format': format,
        'format_width': width,
        'format_height': height,
    }



@register.inclusion_tag('front/includes/carousel.html', takes_context=True)
def display_carousel(context, format, page, location, identifier=None):
    """
    Displays a carousel related to its format, its page and its location.
    
    """
    # Gets campaign if it exists
    if context.has_key('campaign'):
        campaign = context['campaign']
    else:
        campaign = None
    
    # Gets width and height
    width, height = format.split('x')
    today = datetime.date.today()
    try:
        carousel = AdCarousel.objects.filter(
            positions__format__width=width, 
            positions__format__height=height,
            positions__page__slug=page, 
            positions__location__position=location)
        if campaign:
            carousel = carousel.filter(campaign=campaign)[0:1].get()
        else:
            carousel = carousel.filter(starting_date__lte=datetime.date.today(), ending_date__gte=datetime.date.today())[0:1].get()
    except ObjectDoesNotExist:
        carousel = None
    return {
        'MEDIA_URL': context['MEDIA_URL'],
        'carousel': carousel,
        'format': format,
        'format_width': width,
        'format_height': height,
        'identifier': identifier,
    }


@register.simple_tag
def calculate_banner_total(count_days, price):
    """
    Calculate banner total price.
    
    """
    if price is None:
        return Decimal('0.00')
    else:
        price_per_day = price / 30
        total = count_days * price_per_day
        return total.quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)


@register.simple_tag
def calculate_campaign_banners_total(obj):
    """
    Calculates campaign total price.
    
    """
    banners = obj.adbanner_set.all()
    total = Decimal('0')
    for banner in banners:
        for position in banner.positions.all():
            total += calculate_banner_total(banner.count_days(), position.price)
    return total.quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)


@register.simple_tag
def calculate_campaign_carousels_total(obj):
    """
    Calculates campaign carousels total price.
    
    """
    carousels = obj.adcarousel_set.all()
    total = Decimal('0')
    for carousel in carousels:
        for position in carousel.positions.all():
            total += calculate_banner_total(carousel.count_days(), position.price)
    return total.quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)


@register.simple_tag
def calculate_campaign_total(obj):
    """
    Calculates campaign total.
    
    """
    total = Decimal('0')
    if obj.adbanner_set.all():
        total += calculate_campaign_banners_total(obj)
    if obj.adcarousel_set.all():
        total += calculate_campaign_carousels_total(obj)
    return total


