# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.ads_preview`` application.

"""
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from critica.apps.front.views import home
from critica.apps.front.views import category
from critica.apps.front.views import regions
from critica.apps.front.views import voyages
from critica.apps.front.views import epicurien
from critica.apps.front.views import anger
from critica.apps.ads.models import AdCampaign


def _get_campaign(campaign_id):
    """
    Returns campaign object.
    
    """
    try:
        campaign = AdCampaign.objects.get(pk=campaign_id)
    except ObjectDoesNotExist:
        campaign = None
    return campaign


@login_required
def preview_home(request, campaign_id):
    """
    Displays ads preview on the homepage.
    
    """
    extra_context = {}
    extra_context['campaign'] = _get_campaign(campaign_id)
    
    return home(
        request, 
        issue=None,
        is_ads_preview=True,
        extra_context=extra_context,
    )


@login_required
def preview_category(request, campaign_id, category_slug):
    """
    Displays ads preview on a given category.
    
    """
    extra_context = {}
    extra_context['campaign'] = _get_campaign(campaign_id)
    
    return category(
        request, 
        category_slug=category_slug, 
        issue=None, 
        is_ads_preview=True,
        extra_context=extra_context,
    )


@login_required
def preview_category_regions(request, campaign_id):
    """
    Displays ads preview on "Regions" category.
    
    """
    extra_context = {}
    extra_context['campaign'] = _get_campaign(campaign_id)

    return regions(
        request, 
        issue=None, 
        is_ads_preview=True, 
        extra_context=extra_context,
    )
    

@login_required
def preview_category_voyages(request, campaign_id):
    """
    Displays ads preview on "Voyages" category.
    
    """
    extra_context = {}
    extra_context['campaign'] = _get_campaign(campaign_id)
    
    return voyages(
        request, 
        issue=None, 
        is_ads_preview=True, 
        extra_context=extra_context,
    )
    

@login_required
def preview_category_epicurien(request, campaign_id):
    """
    Displays ads preview on "Epicurien" category.
    
    """
    extra_context = {}
    extra_context['campaign'] = _get_campaign(campaign_id)
    
    return epicurien(
        request, 
        issue=None, 
        is_ads_preview=True, 
        extra_context=extra_context,
    )


@login_required
def preview_category_anger(request, campaign_id):
    """
    Displays ads preview on "Anger" category.
    
    """
    extra_context = {}
    extra_context['campaign'] = _get_campaign(campaign_id)
    
    return anger(
        request, 
        issue=None, 
        is_ads_preview=True, 
        extra_context=extra_context,
    )



