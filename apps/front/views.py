# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.front`` application.

"""
from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.views.generic.simple import direct_to_template
from tagging.models import Tag
from tagging.models import TaggedItem
from tagging.utils import calculate_cloud
from critica.apps.categories.models import Category
from critica.apps.issues.models import Issue
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.positions.models import IssueNotePosition
from critica.apps.articles.models import Article
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.epicurien.models import EpicurienArticleType
from critica.apps.epicurien import settings as epicurien_settings
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.voyages import settings as voyages_settings
from critica.apps.anger.models import AngerArticle
from critica.apps.anger import settings as anger_settings
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.regions.models import FeaturedRegion
from critica.apps.illustrations.models import IllustrationOfTheDay
from critica.apps.videos.models import Video
from critica.apps.ads.models import AdBannerPosition
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarouselPosition
from critica.apps.ads.models import AdCarousel
from critica.apps.issues.views import _get_current_issue


# HOME
# ------------------------------------------------------------------------------
def home(request, **kwargs):
    """
    Displays the Homepage.
    
    """
    # Initialize context
    # --------------------------------------------------------------------------
    context = _initialize_context(kwargs)
    issue = context['issue']
        
    # Poll
    # --------------------------------------------------------------------------
    from critica.apps.polls.models import Poll
    from critica.apps.polls.models import Choice
    from critica.apps.polls.models import Vote
    if request.method == 'POST':
        if request.POST.has_key('poll'):
            poll = Poll.objects.get(pk=request.POST['id_poll'])
            choice = Choice.objects.get(pk=request.POST['id_choice'])
            ip_address = request.POST['ip_address']
            vote = Vote(poll=poll, choice=choice, ip_address=ip_address)
            vote.save()

    # Articles
    # --------------------------------------------------------------------------
    category_positions = IssueCategoryPosition.objects.filter(issue=issue)
    for category_position in category_positions:
        if category_position.position is not None:
            varname = 'article_%s' % category_position.position.id
            if context['is_preview']:
                try:
                    article = Article.preview.filter(issues__id=issue.id, category=category_position.category)
                    context[varname] = article[0:1].get()
                except ObjectDoesNotExist:
                    context[varname] = None
            else:  
                try:
                    article = Article.published.filter(issues__id=issue.id, category=category_position.category)
                    article = article[0:1].get()
                    context[varname] = article
                except ObjectDoesNotExist:
                    context[varname] = None

    # Regions
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['region_note'] = RegionNote.preview.get_featured(issue_id=issue.id)
    else:
        context['region_note'] = RegionNote.published.get_featured(issue_id=issue.id)

    # Voyages
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['voyages_article'] = VoyagesArticle.preview.issue_article(issue_id=issue.id)
    else:
        context['voyages_article'] = VoyagesArticle.published.issue_article(issue_id=issue.id)
    
    # Epicurien
    # --------------------------------------------------------------------------
    epicurien_articles = []
    if context['is_preview']:
        a = EpicurienArticle.preview.issue_article_cotegourmets(issue_id=issue.id)
        epicurien_articles.append(a)
        a = EpicurienArticle.preview.issue_article_cotebar(issue_id=issue.id)
        epicurien_articles.append(a)
        a = EpicurienArticle.preview.issue_article_cotefumeurs(issue_id=issue.id)
        epicurien_articles.append(a)
    else:
        a = EpicurienArticle.published.issue_article_cotegourmets(issue_id=issue.id)
        epicurien_articles.append(a)
        a = EpicurienArticle.published.issue_article_cotebar(issue_id=issue.id)
        epicurien_articles.append(a)
        a = EpicurienArticle.published.issue_article_cotefumeurs(issue_id=issue.id)
        epicurien_articles.append(a)
    context['epicurien_articles'] = epicurien_articles
    
    # Anger
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['anger_article'] = AngerArticle.preview.issue_article(issue_id=issue.id)
    else:
        context['anger_article'] = AngerArticle.published.issue_article(issue_id=issue.id)
    
    # Illustration of the day
    # --------------------------------------------------------------------------
    context['illustration'] = IllustrationOfTheDay.objects.issue_illustration(issue_id=issue.id)

    # Video
    # --------------------------------------------------------------------------
    context['video'] = Video.published.issue_video(issue_id=issue.id)
        
    # Tag cloud
    # --------------------------------------------------------------------------
    all_tags = []
    article_tags = Tag.objects.usage_for_queryset(Article.published.all(), counts=True)
    for tag in article_tags:
        all_tags.append(tag)
        
    note_tags = Tag.objects.usage_for_queryset(Note.published.all(), counts=True)
    for tag in note_tags:
        all_tags.append(tag)
    
    region_tags = Tag.objects.usage_for_queryset(RegionNote.published.all(), counts=True)
    for tag in region_tags:
        all_tags.append(tag)
        
    voyages_tags = Tag.objects.usage_for_queryset(VoyagesArticle.published.all(), counts=True)
    for tag in voyages_tags:
        all_tags.append(tag)
        
    epicurien_tags = Tag.objects.usage_for_queryset(VoyagesArticle.published.all(), counts=True)
    for tag in epicurien_tags:
        all_tags.append(tag)
        
    anger_tags = Tag.objects.usage_for_queryset(AngerArticle.published.all(), counts=True)
    for tag in anger_tags:
        all_tags.append(tag)
        
    tags = calculate_cloud(all_tags, steps=10)
    if len(tags) <= 50:
        tagcloud = tags
    else:
        tagcloud = []
        for tag in tags:
            if tag.count > 2:
                tagcloud.append(tag)
    context['tagcloud'] = tagcloud[:50]
    
    return direct_to_template(request, 'front/home.html', context)


# CATEGORY
# ------------------------------------------------------------------------------
def category(request, category_slug, **kwargs):
    """
    Displays the given category page.
    
    """
    # Initialize context
    # --------------------------------------------------------------------------
    context = _initialize_context(kwargs)
    issue = context['issue']
    
    # Category
    # --------------------------------------------------------------------------
    category = get_object_or_404(Category, slug=category_slug)
    context['category'] = category
    
    # Auto-increment view count
    # --------------------------------------------------------------------------
    if context['is_current'] or context['is_archive']:
        articles = Article.published.filter(issues__id=issue.id, category=category)
        for article in articles:
            article.view_count += 1
            article.save()
        notes = Note.published.filter(issues__id=issue.id, category=category)
        for note in notes:
            note.view_count += 1
            note.save()

    # Notes
    # --------------------------------------------------------------------------
    note_positions = IssueNotePosition.objects.filter(issue=issue, category=category)
    for note_position in note_positions:
        if note_position.position is not None:
            varname = 'note_%s' % note_position.position.id
            if context['is_preview']:
                try:
                    note = Note.preview.filter(issues__id=issue.id, type=note_position.type, category=category)
                    note = note.order_by('-publication_date')
                    note = note[0:1].get()
                    context[varname] = note
                except ObjectDoesNotExist:
                    context[varname] = None
            else:
                try:
                    note = Note.published.filter(issues__id=issue.id, type=note_position.type, category=category)
                    note = note.order_by('-publication_date')
                    note = note[0:1].get()
                    context[varname] = note
                except ObjectDoesNotExist:
                    context[varname] = None
                    
    # Article
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['article'] = Article.preview.category_article(
            issue_id=issue.id, 
            category_id=category.id)
    else:
        context['article'] = Article.published.category_article(
            issue_id=issue.id, 
            category_id=category.id)
    
    return direct_to_template(request, 'front/category.html', context)


# REGIONS
# ------------------------------------------------------------------------------
def regions(request, **kwargs):
    """
    Displays "Regions" category page.
    
    """
    # Initialize context
    # --------------------------------------------------------------------------
    context = _initialize_context(kwargs)
    issue = context['issue']
    
    # Auto-increment view count
    # --------------------------------------------------------------------------
    if context['is_current'] or context['is_archive']:
        notes = RegionNote.published.filter(issues__id=issue.id)
        for note in notes:
            note.view_count += 1
            note.save()
    
    # Notes
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['featured_region_note'] = RegionNote.preview.get_featured(issue_id=issue.id)
        regions_notes = RegionNote.preview.get_notes(issue_id=issue.id, excluded_obj=context['featured_region_note'])
    else:
        context['featured_region_note'] = RegionNote.published.get_featured(issue_id=issue.id)
        regions_notes = RegionNote.published.get_notes(issue_id=issue.id, excluded_obj=context['featured_region_note'])
        
    context['regions_notes_1'] = regions_notes[0:10]
    context['regions_notes_2'] = regions_notes[10:20]
    context['regions_notes_3'] = regions_notes[20:]
    
    return direct_to_template(request, 'front/regions.html', context)


# VOYAGES
# ------------------------------------------------------------------------------
def voyages(request, **kwargs):
    """
    Displays "Voyages" category page.
    
    """
    # Initialize context
    # --------------------------------------------------------------------------
    context = _initialize_context(kwargs)
    issue = context['issue']
    
    # Auto-increment view count
    # --------------------------------------------------------------------------
    if context['is_current'] or context['is_archive']:
        articles = VoyagesArticle.published.filter(issues__id=issue.id)
        for article in articles:
            article.view_count += 1
            article.save()    
    
    # Articles
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['article'] = VoyagesArticle.preview.issue_article(issue_id=issue.id)
        context['archives'] = VoyagesArticle.preview.latest(
            limit=voyages_settings.MAX_ARCHIVES,
            excluded_obj=context['article'])
    else:
        context['article'] = VoyagesArticle.published.issue_article(issue_id=issue.id)
        context['archives'] = VoyagesArticle.published.latest(
            limit=voyages_settings.MAX_ARCHIVES,
            excluded_obj=context['article'])
        
    return direct_to_template(request, 'front/voyages.html', context)


# EPICURIEN
# ------------------------------------------------------------------------------
def epicurien(request, **kwargs):
    """
    Displays "Epicurien" category page.
    
    """
    # Initialize context
    # --------------------------------------------------------------------------
    context = _initialize_context(kwargs)
    issue = context['issue']
        
    # Auto-increment view count
    # --------------------------------------------------------------------------
    if context['is_current'] or context['is_archive']:
        epicurien_articles = EpicurienArticle.published.filter(issues__id=issue.id)
        for article in epicurien_articles:
            article.view_count += 1
            article.save()
    
    # Côté fumeurs
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['article_cotefumeurs'] = EpicurienArticle.preview.issue_article_cotefumeurs(issue_id=issue.id)
        context['archives_cotefumeurs'] = EpicurienArticle.preview.latest(
            type_id=3,
            limit=epicurien_settings.MAX_ARCHIVES,
            excluded_obj=context['article_cotefumeurs'])
    else:
        context['article_cotefumeurs'] = EpicurienArticle.published.issue_article_cotefumeurs(issue_id=issue.id)
        context['archives_cotefumeurs'] = EpicurienArticle.published.latest(
            type_id=3,
            limit=epicurien_settings.MAX_ARCHIVES,
            excluded_obj=context['article_cotefumeurs'])
            
    # Côté Gourmets
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['article_cotegourmets'] = EpicurienArticle.preview.issue_article_cotegourmets(issue_id=issue.id)
        context['archives_cotegourmets'] = EpicurienArticle.preview.latest(
            type_id=1,
            limit=epicurien_settings.MAX_ARCHIVES,
            excluded_obj=context['article_cotegourmets'])
    else:
        context['article_cotegourmets'] = EpicurienArticle.published.issue_article_cotegourmets(issue_id=issue.id)
        context['archives_cotegourmets'] = EpicurienArticle.published.latest(
            type_id=1,
            limit=epicurien_settings.MAX_ARCHIVES,
            excluded_obj=context['article_cotegourmets'])
    
    # Côté Bar
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['article_cotebar'] = EpicurienArticle.preview.issue_article_cotebar(issue_id=issue.id)
        context['archives_cotebar'] = EpicurienArticle.preview.latest(
            type_id=2,
            limit=epicurien_settings.MAX_ARCHIVES,
            excluded_obj=context['article_cotebar'])
    else:
        context['article_cotebar'] = EpicurienArticle.published.issue_article_cotebar(issue_id=issue.id)
        context['archives_cotebar'] = EpicurienArticle.published.latest(
            type_id=2,
            limit=epicurien_settings.MAX_ARCHIVES,
            excluded_obj=context['article_cotebar'])

    return direct_to_template(request, 'front/epicurien.html', context)


# ANGER
# ------------------------------------------------------------------------------
def anger(request, **kwargs):
    """
    Displays "Anger" (Coup de Gueule) category page.
    
    """
    # Initialize context
    # --------------------------------------------------------------------------
    context = _initialize_context(kwargs)
    issue = context['issue']
    
    # Auto-increment view count
    # --------------------------------------------------------------------------
    if context['is_current'] or context['is_archive']:
        articles = AngerArticle.published.filter(issues__id=issue.id)
        for article in articles:
            article.view_count += 1
            article.save()

    # Articles
    # --------------------------------------------------------------------------
    if context['is_preview']:
        context['article'] = AngerArticle.preview.issue_article(issue_id=issue.id)
        context['archives'] = AngerArticle.preview.latest(
            limit=anger_settings.MAX_ARCHIVES,
            excluded_obj=context['article'])
    else:
        context['article'] = AngerArticle.published.issue_article(issue_id=issue.id)
        context['archives'] = AngerArticle.published.latest(
            limit=anger_settings.MAX_ARCHIVES,
            excluded_obj=context['article'])
        
    return direct_to_template(request, 'front/anger.html', context)


# Useful private functions
# ------------------------------------------------------------------------------
def _initialize_context(kwarg_dict):
    """
    Initialize context.
    
    """
    issue = None
    if 'issue' in kwarg_dict:
        issue = kwarg_dict['issue']
    
    is_preview = None
    if 'is_preview' in kwarg_dict:
        is_preview = kwarg_dict['is_preview']
    
    is_archive = None
    if 'is_archive' in kwarg_dict:
        is_archive = kwarg_dict['is_archive']
    
    is_ads_preview = None
    if 'is_ads_preview' in kwarg_dict:
        is_ads_preview = kwarg_dict['is_ads_preview']
    
    extra_context = None
    if 'extra_context' in kwarg_dict:
        extra_context = kwarg_dict['extra_context']

    # Update context with extra_context
    # --------------------------------------------------------------------------
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    #---------------------------------------------------------------------------
    if not issue:
        issue = _get_current_issue()
    context['issue'] = issue
    
    # Is a preview mode?
    # --------------------------------------------------------------------------
    context['is_preview'] = False
    if is_preview:
        context['is_preview'] = True
    
    # Is a ads preview mode?
    # --------------------------------------------------------------------------
    context['is_ads_preview'] = False
    if is_ads_preview:
        context['is_ads_preview'] = True
        
    # Is an archive mode?
    # --------------------------------------------------------------------------
    context['is_archive'] = False
    if is_archive:
        context['is_archive'] = True

    # Is a current mode?
    # --------------------------------------------------------------------------
    context['is_current'] = False
    if not context['is_preview'] and not context['is_archive'] and not context['is_ads_preview']:
        context['is_current'] = True
        
    return context


