"""
Views of ``critica.apps.ads_dashboard`` application.

"""
from django.views.generic.simple import direct_to_template


def index(request, campaign=None):
    """
    View of ads dashboard.
    
    By default, displays dashboard of the latest campaign. If campaign is defined, 
    displays the dashboard for this campaign.
    
    """
    context = {}
    context['root_path'] = '/admin/'
    return direct_to_template(request, 'ads_dashboard/index.html', context)
