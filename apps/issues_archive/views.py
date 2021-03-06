# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.issues_archive`` application.

"""
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage
from critica.apps.front.views import home
from critica.apps.front.views import category
from critica.apps.front.views import regions
from critica.apps.front.views import voyages
from critica.apps.front.views import epicurien
from critica.apps.front.views import anger
from critica.apps.issues.models import Issue
from critica.apps.issues.views import _get_current_issue


def index(request):
    """
    View of archive list.
    
    """
    issue = _get_current_issue()
    context = {}   
    context['issue'] = issue
    context['is_current'] = True
    try:
        item_list = Issue.objects.filter(is_published=True).order_by('-publication_date')
    except ObjectDoesNotExist:
        item_list = None
    paginator = Paginator(item_list, 30)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        context['items'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        context['items'] = paginator.page(paginator.num_pages)
    return direct_to_template(request, 'issues_archive/index.html', context)
    

def archive_home(request, issue_number):
    """
    Displays home archive of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return home(request, issue=issue, is_archive=True)


def archive_category(request, issue_number, category_slug):
    """
    Displays category archive of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return category(request, category_slug, issue=issue, is_archive=True)


def archive_category_regions(request, issue_number):
    """
    Displays "Regions" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return regions(request, issue=issue, is_archive=True)


def archive_category_voyages(request, issue_number):
    """
    Displays "Voyages" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return voyages(request, issue=issue, is_archive=True)


def archive_category_epicurien(request, issue_number):
    """
    Displays "Epicurien" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return epicurien(request, issue=issue, is_archive=True)


def archive_category_anger(request, issue_number):
    """
    Displays "Anger" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return anger(request, issue=issue, is_archive=True)



