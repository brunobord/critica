# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.front`` application.

"""
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.categories.models import Category
from critica.apps.issues.models import Issue
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.positions.models import IssueNotePosition
from critica.apps.articles.models import Article
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.epicurien.models import EpicurienArticleType
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.anger.models import AngerArticle
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.regions.models import FeaturedRegion
from critica.apps.illustrations.models import IllustrationOfTheDay
from critica.apps.videos.models import Video


def _get_current_issue():
    """
    Gets the current issue.
    
    """
    issues = Issue.objects.filter(is_published=True)[:1]
    issue = Issue.objects.get(id=1)
    return issue


def home(request):
    """
    Displays the homepage.
    
    """
    # Gets the current issue
    issue = _get_current_issue()
    
    # Initializes context dictionary
    context = {}

    # Generic articles
    # --------------------------------------------------------------------------
    category_positions = IssueCategoryPosition.objects.filter(issue=issue)
    for category_position in category_positions:
        if category_position.position is not None:
            varname = 'article_%s' % category_position.position.id
            try:
                article = Article.objects.get(
                issues__id=issue.id, 
                is_ready_to_publish=True, 
                is_reserved=False, 
                category=category_position.category)
                context[varname] = article
            except ObjectDoesNotExist:
                context[varname] = False

    # Regions
    # --------------------------------------------------------------------------
    try:
        featured = FeaturedRegion.objects.get(issue=issue)
        context['region_note'] = RegionNote.objects.get(
            issues__id=issue.id, 
            is_ready_to_publish=True, 
            is_reserved=False, 
            region=featured.region)
    except ObjectDoesNotExist:
        context['region_note'] = False

    # Voyages
    # --------------------------------------------------------------------------
    try:
        context['voyages_article'] = VoyagesArticle.objects.get(
            issues__id=issue.id, 
            is_ready_to_publish=True, 
            is_reserved=False)
    except ObjectDoesNotExist:
        context['voyages_article'] = False
    
    # Epicurien
    # --------------------------------------------------------------------------
    try:
        context['epicurien_articles'] = EpicurienArticle.objects.filter(
            issues__id=issue.id, 
            is_ready_to_publish=True, 
            is_reserved=False)
    except ObjectDoesNotExist:
        context['epicurien_articles'] = False
    
    # Anger ("Coup de Gueule")
    # --------------------------------------------------------------------------
    try:
        context['anger_article'] = AngerArticle.objects.get(
            issues__id=issue.id, 
            is_ready_to_publish=True, 
            is_reserved=False)
    except ObjectDoesNotExist:
        context['anger_article'] = False
    
    # Illustration of the day
    # --------------------------------------------------------------------------
    try:
        context['illustration'] = IllustrationOfTheDay.objects.get(
            issues__id=issue.id)
    except ObjectDoesNotExist:
        context['illustration'] = False

    # Video (reportage)
    # --------------------------------------------------------------------------
    try:
        context['video'] = Video.objects.get(issues__id=issue.id)
    except ObjectDoesNotExist:
        context['video'] = False

    return render_to_response(
        'front/home.html', 
        context, 
        context_instance=RequestContext(request))



def category(request, category_slug):
    """
    Displays the given category page.
    
    """
    issue = _get_current_issue()
    context = {}
    
    category = get_object_or_404(Category, slug=category_slug)
    context['category'] = category

    note_positions = IssueNotePosition.objects.filter(issue=issue, category=category)
    for note_position in note_positions:
        if note_position.position is not None:
            varname = 'note_%s' % note_position.position.id
            try:
                note = Note.objects.get(
                    issues__id=issue.id, 
                    is_ready_to_publish=True, 
                    is_reserved=False, 
                    type=note_position.type,
                    category=category)
                context[varname] = note
            except ObjectDoesNotExist:
                context[varname] = False
    context['article'] = Article.objects.get(issues__id=issue.id, category__slug=category_slug)
    
    return render_to_response(
        'front/category.html', 
        context,
        context_instance=RequestContext(request))
        
        
def regions(request):
    """
    Displays "Regions" category page.
    
    """
    issue = _get_current_issue()
    context = {}
    featured_region = FeaturedRegion.objects.get(issue=issue)
    featured_region_note = RegionNote.objects.get(
        issues__id=issue.id,
        is_ready_to_publish=True,
        is_reserved=False,
        region=featured_region.region)
    regions_notes = RegionNote.objects.filter(
        issues__id=issue.id,
        is_ready_to_publish=True, 
        is_reserved=False).exclude(id=featured_region.id).order_by('region__name')
    
    context['featured_region'] = featured_region
    context['featured_region_note'] = featured_region_note
    context['regions_notes_1'] = regions_notes[0:10]
    context['regions_notes_2'] = regions_notes[10:20]
    context['regions_notes_3'] = regions_notes[20:]
    
    return render_to_response(
        'front/regions.html',
        context,
        context_instance=RequestContext(request))


def voyages(request):
    """
    Displays "Voyages" category page.
    
    """
    issue = _get_current_issue()
    context = {}
    
    try:
        context['article'] = VoyagesArticle.objects.get(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False)
    except ObjectDoesNotExist:
        context['article'] = False
        
    return render_to_response(
        'front/voyages.html',
        context,
        context_instance=RequestContext(request))


def epicurien(request):
    """
    Displays "Epicurien" category page.
    
    """
    issue = _get_current_issue()
    context = {}
    
    type_cotefumeurs = EpicurienArticleType.objects.get(slug='cote-fumeurs')
    type_cotegourmets = EpicurienArticleType.objects.get(slug='cote-gourmets')
    type_cotebar = EpicurienArticleType.objects.get(slug='cote-bar')
    
    # Côté fumeurs
    # --------------------------------------------------------------------------
    try:
        context['article_cotefumeurs'] = EpicurienArticle.objects.get(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False,
            type=type_cotefumeurs)
    except ObjectDoesNotExist:
        context['article_cotefumeurs'] = False
        
    try:
        context['archives_cotefumeurs'] = EpicurienArticle.objects.filter(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False,
            type=type_cotefumeurs)[:10]
    except ObjectDoesNotExist:
        context['archives_cotefumeurs'] = False
    
    # Côté Gourmets
    # --------------------------------------------------------------------------
    try:
        context['article_cotegourmets'] = EpicurienArticle.objects.get(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False,
            type=type_cotegourmets)
    except ObjectDoesNotExist:
        context['article_cotegourmets'] = False
        
    try:
        context['archives_cotegourmets'] = EpicurienArticle.objects.filter(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False,
            type=type_cotegourmets)[:10]
    except ObjectDoesNotExist:
        context['archives_cotegourmets'] = False
    
    # Côté Bar
    # --------------------------------------------------------------------------
    try:
        context['article_cotebar'] = EpicurienArticle.objects.get(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False,
            type=type_cotebar)
    except ObjectDoesNotExist:
        context['article_cotebar'] = False
        
    try:
        context['archives_cotebar'] = EpicurienArticle.objects.filter(
            issues__id=issue.id,
            is_ready_to_publish=True,
            is_reserved=False,
            type=type_cotebar)[:10]
    except ObjectDoesNotExist:
        context['archives_cotebar'] = False

    return render_to_response(
        'front/epicurien.html',
        context,
        context_instance=RequestContext(request))

