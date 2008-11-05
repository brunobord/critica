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
    # Get latest campaign
    try:
        latest_campaign = AdCampaign.objects.order_by('-id')[0:1].get()
    except ObjectDoesNotExist:
        latest_campaign = None
    context['latest_campaign'] = latest_campaign
    # Get other campaigns
    if latest_campaign:
        context['campaigns'] = AdCampaign.objects.order_by('-id')

    return direct_to_template(request, 'ads_dashboard/index.html', context)
