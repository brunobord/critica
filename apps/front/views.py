# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.front`` application.

"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.issues.models import Issue
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.articles.models import Article
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.epicurien.models import EpicurienArticleType
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.anger.models import AngerArticle
from critica.apps.regions.models import RegionNote
from critica.apps.regions.models import FeaturedRegion
from critica.apps.illustrations.models import IllustrationOfTheDay
from critica.apps.videos.models import Video
from tagging.models import Tag
from tagging.utils import calculate_cloud
from tagging.utils import LOGARITHMIC


def home(request):
    """
    Displays the homepage.
    
    """
    issues = Issue.objects.filter(is_published=True)[:1]
    issue = Issue.objects.get(id=1)
    category_positions = IssueCategoryPosition.objects.filter(issue=issue)
    
    context = {}

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

    try:
        featured = FeaturedRegion.objects.get(issue=issue)
        context['region_note'] = RegionNote.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, region=featured.region)
    except ObjectDoesNotExist:
        context['region_note'] = False

    try:
        context['voyages_article'] = VoyagesArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
    except ObjectDoesNotExist:
        context['voyages_article'] = False
        
    try:
        type = EpicurienArticleType.objects.get(id=3)
        context['epicurien_cotefumeur_article'] = EpicurienArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type)
    except ObjectDoesNotExist:
        context['epicurien_cotefumeur_article'] = False
    
    try:
        type = EpicurienArticleType.objects.get(id=1)
        context['epicurien_cotegourmet_article'] = EpicurienArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type)
    except ObjectDoesNotExist:
        context['epicurien_cotegourmet_article'] = False

    try:
        type = EpicurienArticleType.objects.get(id=2)
        context['epicurien_cotebar_article'] = EpicurienArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type)
    except ObjectDoesNotExist:
        context['epicurien_cotebar_article'] = False
        
    try:
        context['anger_article'] = AngerArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
    except ObjectDoesNotExist:
        context['anger_article'] = False
        
    try:
        context['illustration'] = IllustrationOfTheDay.objects.get(issues__id=issue.id)
    except ObjectDoesNotExist:
        context['illustration'] = False

    try:
        context['video'] = Video.objects.get(issues__id=issue.id)
    except ObjectDoesNotExist:
        context['video'] = False
        
        
    return render_to_response('front/home.html', context, context_instance=RequestContext(request))


def category(request, category_slug):
    """
    Displays the given category.
    
    """
    return render_to_response(
        'front/category.html', 
        {},
        context_instance=RequestContext(request))
