# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.ads`` application.

"""
import datetime
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



@register.inclusion_tag('front/includes/carousel.html')
def display_carousel(format, page, location):
    """
    Displays a carousel related to its format, its page and its location.
    
    """
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


@register.simple_tag
def calculate_banner_total(count_days, price):
    """
    Calculate banner total price.
    
    """
    from decimal import getcontext
    from decimal import Decimal
    from decimal import ROUND_HALF_EVEN
    price_per_day = price / 30
    total = count_days * price_per_day
    return total.quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)


@register.simple_tag
def calculate_campaign_total(obj):
    """
    Calculates campaign total price.
    
    """
    from decimal import getcontext
    from decimal import Decimal
    from decimal import ROUND_HALF_EVEN
    banners = obj.adbanner_set.all()
    total = Decimal('0')
    for banner in banners:
        for position in banner.positions.all():
            total += calculate_banner_total(banner.count_days(), position.price)
    return total.quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)


