# -*- coding: utf-8 -*-
"""
Custom admins views.

"""
import datetime
from django import http, template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.issues.models import Issue
from critica.apps.categories.models import Category
from critica.apps.articles.models import Article
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.anger.models import AngerArticle
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.quotas.models import CategoryQuota


@login_required
@never_cache
def basic_dashboard(request, issue=None):
    """
    Basic admin dashboard view.
    
    """ 
    context = {}
    
    # Issue
    # --------------------------------------------------------------------------
    if issue is not None:
        current_issue = Issue.objects.get(number=issue)
        context['specific_issue'] = True
    else:
        try:
            current_issue = Issue.objects.get(publication_date=datetime.date.today())
        except ObjectDoesNotExist:
            current_issue = Issue.objects.get(pk=1)
    context['current_issue'] = current_issue
    
    # All issues
    # --------------------------------------------------------------------------
    context['issues'] = Issue.objects.all().order_by('-number')
    
    # Standard categories
    # --------------------------------------------------------------------------
    EXCLUDED_CATEGORIES = ['epicurien', 'voyages', 'coup-de-gueule', 'regions']
    categories = Category.objects.exclude(slug__in=EXCLUDED_CATEGORIES)
    std_categories = []
    for category in categories:
        articles_count = Article.objects.filter(
            issues__id=current_issue.id,
            is_ready_to_publish=True,
            is_reserved=False, 
            category=category).count()
        notes_count = Note.objects.filter(
            issues__id=current_issue.id, 
            is_ready_to_publish=True,
            is_reserved=False,
            category=category).count()
        # Total count
        total_count = articles_count + notes_count
        # Article and note quotas
        category_quota = CategoryQuota.objects.get(issue=current_issue, category=category)
        # Note quotas
        notes_quota = category_quota.quota - 1
        # Complete flag
        if total_count >= category_quota.quota:
            is_complete = True
        else:
            is_complete = False
        std_categories.append(
            [
                category, 
                total_count, 
                notes_count, 
                category_quota.quota,
                notes_quota,
                is_complete,
            ]
        )
    context['std_categories'] = std_categories
    
    # Regions
    # --------------------------------------------------------------------------
    regions_category = Category.objects.get(slug='regions')
    regions_count = RegionNote.objects.filter(
        issues__id=current_issue.id,
        is_ready_to_publish=True,
        is_reserved=False).count()
    regions_quota = CategoryQuota.objects.get(issue=current_issue, category=regions_category)
    if regions_count >= regions_quota.quota:
        regions_complete = True
    else:
        regions_complete = False
    context['regions_count'] = regions_count
    context['regions_quota'] = regions_quota.quota
    context['regions_complete'] = regions_complete
    
    # Voyages
    # --------------------------------------------------------------------------
    voyages_category = Category.objects.get(slug='voyages')
    voyages_count = VoyagesArticle.objects.filter(
        issues__id=current_issue.id,
        is_ready_to_publish=True,
        is_reserved=False).count()
    voyages_quota = CategoryQuota.objects.get(issue=current_issue, category=voyages_category)
    if voyages_count >= voyages_quota.quota:
        voyages_complete = True
    else:
        voyages_complete = False
    context['voyages_count'] = voyages_count
    context['voyages_quota'] = voyages_quota.quota
    context['voyages_complete'] = voyages_complete
    
    # Epicurien
    # --------------------------------------------------------------------------
    epicurien_category = Category.objects.get(slug='epicurien')
    epicurien_count = EpicurienArticle.objects.filter(
        issues__id=current_issue.id,
        is_ready_to_publish=True,
        is_reserved=False).count()
    epicurien_quota = CategoryQuota.objects.get(issue=current_issue, category=epicurien_category)
    if epicurien_count >= epicurien_quota.quota:
        epicurien_complete = True
    else:
        epicurien_complete = False
    context['epicurien_count'] = epicurien_count
    context['epicurien_quota'] = epicurien_quota.quota
    context['epicurien_complete'] = epicurien_complete

    # Coup de Gueule
    # --------------------------------------------------------------------------
    anger_category = Category.objects.get(slug='coup-de-gueule')
    anger_count = AngerArticle.objects.filter(
        issues__id=current_issue.id,
        is_ready_to_publish=True,
        is_reserved=False).count()
    anger_quota = CategoryQuota.objects.get(issue=current_issue, category=anger_category)
    if anger_count >= anger_quota.quota:
        anger_complete = True
    else:
        anger_complete = False
    context['anger_count'] = anger_count
    context['anger_quota'] = anger_quota.quota
    context['anger_complete'] = anger_complete

    return render_to_response(
        'basic_admin/current_issue/dashboard/index.html', 
        context, 
        context_instance=RequestContext(request)
    )




