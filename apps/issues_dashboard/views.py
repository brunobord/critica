# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.issues_dashboard`` application.

"""
import datetime
from django import http, template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.sites.models import Site
from django.views.generic.simple import direct_to_template
from critica.apps.issues.models import Issue
from critica.apps.categories.models import Category
from critica.apps.articles.models import Article
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.epicurien.models import EpicurienArticleType
from critica.apps.anger.models import AngerArticle
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.regions.models import FeaturedRegion
from critica.apps.illustrations.models import IllustrationOfTheDay
from critica.apps.quotas.models import CategoryQuota
from critica.apps.positions.models import DefaultCategoryPosition
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.positions.models import DefaultNotePosition
from critica.apps.positions.models import IssueNotePosition
from critica.apps.polls.models import Poll
from critica.apps.videos.models import Video


@login_required
@permission_required('users.is_administrator')
@permission_required('users.is_editor')
@never_cache
def index(request, issue=None):
    """
    View of issues dashboard.
    
    """ 
    context = {}
    
    # Issue
    # --------------------------------------------------------------------------
    if issue:
        current_issue = Issue.objects.get(number=issue)
        context['specific_issue'] = True
    else:
        try:
            current_issue = Issue.objects.get(publication_date=datetime.date.today())
        except ObjectDoesNotExist:
            current_issue = Issue.objects.order_by('-number')[0:1].get()
    context['issue'] = current_issue
    
    # Current site
    # --------------------------------------------------------------------------
    site = Site.objects.get_current()
    context['site_url'] = 'http://' + site.domain
    
    # All issues
    # --------------------------------------------------------------------------
    context['issues'] = Issue.objects.all().order_by('-number')
    
    # Excluded categories
    # --------------------------------------------------------------------------
    EXCLUDED_CATEGORIES = ['epicurien', 'voyages', 'coup-de-gueule', 'regions']
    
    # Cover
    # --------------------------------------------------------------------------
    cover_articles_quota = Category.objects.exclude(slug__in=EXCLUDED_CATEGORIES).count()
    cover_articles_count = Article.objects.filter(
        issues__id=current_issue.id,
        is_ready_to_publish=True,
        is_reserved=False).count()
    if cover_articles_count >= cover_articles_quota:
        cover_articles_complete = True
    else:
        cover_articles_complete = False
    context['cover_articles_quota'] = cover_articles_quota
    context['cover_articles_count'] = cover_articles_count
    context['cover_articles_complete'] = cover_articles_complete
    
    try:
        cover_illustration = IllustrationOfTheDay.objects.get(issues__id=current_issue.id)
        context['cover_illustration'] = cover_illustration
    except MultipleObjectsReturned:
        cover_illustrations = IllustrationOfTheDay.objects.filter(issues__id=current_issue.id)
        context['cover_illustration_multiple'] = True
        context['cover_illustrations'] = cover_illustrations
    except ObjectDoesNotExist:
        context['cover_illustration'] = None
        
    try:
        cover_anger_article = AngerArticle.objects.get(issues__id=current_issue.id)
        context['cover_anger_article'] = cover_anger_article
    except MultipleObjectsReturned:
        cover_anger_articles = AngerArticle.objects.filter(issues__id=current_issue.id)
        context['cover_anger_multiple'] = True
        context['cover_anger_articles'] = cover_anger_articles
    except ObjectDoesNotExist:
        context['cover_anger_article'] = None
        
    try:
        cover_voyages_article = VoyagesArticle.objects.get(issues__id=current_issue.id)
        context['cover_voyages_article'] = cover_voyages_article
    except MultipleObjectsReturned:
        cover_voyages_articles = VoyagesArticle.objects.filter(issues__id=current_issue.id)
        context['cover_voyages_multiple'] = True
        context['cover_voyages_articles'] = cover_voyages_articles
    except ObjectDoesNotExist:
        context['cover_voyages_article'] = None
    
    epicurien_type_cotegourmets = EpicurienArticleType.objects.get(pk=1)
    try:
        cover_epicurien_cotegourmets_article = EpicurienArticle.objects.get(issues__id=current_issue.id, type=epicurien_type_cotegourmets)
        context['cover_epicurien_cotegourmets_article'] = cover_epicurien_cotegourmets_article
    except MultipleObjectsReturned:
        cover_epicurien_cotegourmets_articles = EpicurienArticle.objects.filter(issues__id=current_issue.id, type=epicurien_type_cotegourmets)
        context['cover_epicurien_cotegourmets_multiple'] = True
        context['cover_epicurien_cotegourmets_articles'] = cover_epicurien_cotegourmets_articles
    except ObjectDoesNotExist:
        context['cover_epicurien_cotegourmets_article'] = None

    epicurien_type_cotebar = EpicurienArticleType.objects.get(pk=2)
    try:
        cover_epicurien_cotebar_article = EpicurienArticle.objects.get(issues__id=current_issue.id, type=epicurien_type_cotebar)
        context['cover_epicurien_cotebar_article'] = cover_epicurien_cotebar_article
    except MultipleObjectsReturned:
        cover_epicurien_cotebar_articles = EpicurienArticle.objects.filter(issues__id=current_issue.id, type=epicurien_type_cotebar)
        context['cover_epicurien_cotebar_multiple'] = True
        context['cover_epicurien_cotebar_articles'] = cover_epicurien_cotebar_articles
    except ObjectDoesNotExist:
        context['cover_epicurien_cotebar_article'] = None

    epicurien_type_cotefumeurs = EpicurienArticleType.objects.get(pk=3)
    try:
        cover_epicurien_cotefumeurs_article = EpicurienArticle.objects.get(issues__id=current_issue.id, type=epicurien_type_cotefumeurs)
        context['cover_epicurien_cotefumeurs_article'] = cover_epicurien_cotefumeurs_article
    except MultipleObjectsReturned:
        cover_epicurien_cotefumeurs_articles = EpicurienArticle.objects.filter(issues__id=current_issue.id, type=epicurien_type_cotefumeurs)
        context['cover_epicurien_cotefumeurs_multiple'] = True
        context['cover_epicurien_cotefumeurs_articles'] = cover_epicurien_cotefumeurs_articles
    except ObjectDoesNotExist:
        context['cover_epicurien_cotefumeurs_article'] = None
        
    try:
        cover_featured_region = FeaturedRegion.objects.get(issue=current_issue)
        context['cover_featured_region'] = cover_featured_region
    except:
        context['cover_featured_region'] = False
        
    # Standard categories
    # --------------------------------------------------------------------------
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
        # position checking
        position_changed = False
        issue_positions = IssueNotePosition.objects.filter(issue=current_issue, category=category)
        default_positions = DefaultNotePosition.objects.filter(category=category)
        for issue_position in issue_positions:
            for default_position in default_positions:
                if issue_position.type == default_position.type:
                    if issue_position.position != default_position.position:
                        position_changed = True
                    
        std_categories.append(
            [
                category, 
                total_count, 
                notes_count, 
                category_quota.quota,
                notes_quota,
                position_changed,
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
    
    # Video
    # --------------------------------------------------------------------------
    try:
        dashboard_video = Video.objects.get(issues__id=current_issue.id)
        context['dashboard_video'] = dashboard_video
    except MultipleObjectsReturned:
        dashboard_videos = Video.objects.filter(issues__id=current_issue.id).order_by('-creation_date')
        context['dashboard_videos_multiple'] = True
        context['dashboard_videos'] = dashboard_videos
    except ObjectDoesNotExist:
        context['dashboard_video'] = None
    
    # Poll
    # --------------------------------------------------------------------------
    try:
        dashboard_poll = Poll.objects.get(issues__id=current_issue.id)
        context['dashboard_poll'] = dashboard_poll
    except MultipleObjectsReturned:
        dashboard_polls = Poll.objects.filter(issues__id=current_issue.id).order_by('-creation_date')
        context['dashboard_polls_multiple'] = True
        context['dashboard_polls'] = dashboard_polls
    except ObjectDoesNotExist:
        context['dashboard_poll'] = None
    
    # Root path
    # --------------------------------------------------------------------------
    context['root_path'] = '/admin/'
    
    return direct_to_template(request, 'issues_dashboard/index.html', context)


@login_required
@permission_required('users.is_administrator')
@permission_required('users.is_editor')
@never_cache
def change_issue_status(request, issue, status):
    """
    Changes issue status: online / offline.
    
    """
    if request.method == 'POST':
        issue = Issue.objects.get(number=issue)
        if int(status) == 1:
            issue.is_published = True
            issue.save()
        if int(status) == 0:
            issue.is_published = False
            issue.save()
    return HttpResponseRedirect(reverse('issues_dashboard_issue', args=[issue]))


