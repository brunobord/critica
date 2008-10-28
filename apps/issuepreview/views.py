# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.issuepreview`` application.

"""
from critica.apps.front.views import home
from critica.apps.front.views import category
from critica.apps.front.views import regions
from critica.apps.front.views import voyages
from critica.apps.front.views import epicurien
from critica.apps.front.views import anger
from critica.apps.issues.views import _get_encoded_issue


def issuepreview_home(request, issue_key):
    """
    Displays home preview of a given issue.
    
    """
    issue = _get_encoded_issue(issue_key)
    return home(request, issue=issue, is_preview=True)



def issuepreview_category(request, issue_key, category_slug):
    """
    Displays category preview of a given issue.
    
    """
    issue = _get_encoded_issue(issue_key)
    return category(request, category_slug=category_slug, issue=issue, is_preview=True)



def issuepreview_regions(request, issue_key):
    """
    Displays "Regions" category of a given issue.
    
    """
    issue = _get_encoded_issue(issue_key)
    return regions(request, issue=issue, is_preview=True)
    
    
    
def issuepreview_voyages(request, issue_key):
    """
    Displays "Voyages" category of a given issue.
    
    """
    issue = _get_encoded_issue(issue_key)
    return voyages(request, issue=issue, is_preview=True)
    
    

def issuepreview_epicurien(request, issue_key):
    """
    Displays "Epicurien" category of a given issue.
    
    """
    issue = _get_encoded_issue(issue_key)
    return epicurien(request, issue=issue, is_preview=True)
    
    

def issuepreview_anger(request, issue_key):
    """
    Displays "Anger" category of a given issue.
    
    """
    issue = _get_encoded_issue(issue_key)
    return anger(request, issue=issue, is_preview=True)


