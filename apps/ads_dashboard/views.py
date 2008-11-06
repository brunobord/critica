"""
Views of ``critica.apps.ads_dashboard`` application.

"""
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.ads.models import AdCampaign


def index(request, campaign=None):
    """
    View of ads dashboard.
    
    By default, displays dashboard of the latest campaign. If campaign is defined, 
    displays the dashboard for this campaign.
    
    """
    context = {}
    context['root_path'] = '/admin/'
    # Gets campaign
    if campaign:
        campaign = AdCampaign.objects.get(pk=campaign)
    else:
        try:
            campaign = AdCampaign.objects.order_by('-id')[0:1].get()
        except ObjectDoesNotExist:
            campaign = None
    context['campaign'] = campaign
    # Gets other campaigns
    try:
        campaigns = AdCampaign.objects.order_by('-id')
    except ObjectDoesNotExist:
        campaigns = None
    context['campaigns'] = campaigns
    
    return direct_to_template(request, 'ads_dashboard/index.html', context)
