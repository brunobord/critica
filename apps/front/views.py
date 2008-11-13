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
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.anger.models import AngerArticle
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


# ------------------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------------------
def home(request, issue=None, is_preview=False, is_archive=False, is_ads_preview=False, extra_context=None):
    """
    Displays the homepage.
    
    """
    # Gets the current issue
    if issue is None:
        issue = _get_current_issue()
    
    # Initializes context dictionary
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    try:
        context['issue'] = issue
    except ObjectDoesNotExist:
        raise Http404
        
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False

    # Is a ads preview
    if is_ads_preview:
        context['is_ads_preview'] = True
    else:
        context['is_ads_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive and not is_ads_preview:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current
        
    # Poll
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

    # Generic articles
    category_positions = IssueCategoryPosition.objects.filter(issue=issue)
    for category_position in category_positions:
        if category_position.position is not None:
            varname = 'article_%s' % category_position.position.id
            if is_preview:
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
    if is_preview:
        try:
            featured = FeaturedRegion.objects.get(issue=issue)
            region_note = RegionNote.preview.filter(issues__id=issue.id, region=featured.region)
            region_note = region_note.order_by('-publication_date')
            region_note = region_note[0:1].get()
            context['region_note'] = region_note
        except ObjectDoesNotExist:
            context['region_note'] = None
    else:
        try:
            featured = FeaturedRegion.objects.get(issue=issue)
            region_note = RegionNote.published.filter(issues__id=issue.id, region=featured.region)
            region_note = region_note.order_by('-publication_date')
            region_note = region_note[0:1].get()
            context['region_note'] = region_note
        except ObjectDoesNotExist:
            context['region_note'] = None

    # Voyages
    if is_preview:
        try:
            voyages_article = VoyagesArticle.preview.filter(issues__id=issue.id)
            voyages_article = voyages_article.order_by('-publication_date')
            voyages_article = voyages_article[0:1].get()
            context['voyages_article'] = voyages_article
        except ObjectDoesNotExist:
            context['voyages_article'] = None
    else:
        try:
            voyages_article = VoyagesArticle.published.filter(issues__id=issue.id)
            voyages_article = voyages_article.order_by('-publication_date')
            voyages_article = voyages_article[0:1].get()
            context['voyages_article'] = voyages_article
        except ObjectDoesNotExist:
            context['voyages_article'] = None
    
    # Epicurien
    if is_preview:
        epicurien_articles = []
        try:
            a = EpicurienArticle.preview.filter(issues__id=issue.id, type__slug='cote-gourmets').order_by('-publication_date')[0:1].get()
            epicurien_articles.append(a)
        except ObjectDoesNotExist:
            pass
        try:
            a = EpicurienArticle.preview.filter(issues__id=issue.id, type__slug='cote-bar').order_by('-publication_date')[0:1].get()
            epicurien_articles.append(a)
        except ObjectDoesNotExist:
            pass
        try:
            a = EpicurienArticle.preview.filter(issues__id=issue.id, type__slug='cote-fumeurs').order_by('-publication_date')[0:1].get()
            epicurien_articles.append(a)
        except ObjectDoesNotExist:
            pass
        context['epicurien_articles'] = epicurien_articles
    else:
        epicurien_articles = []
        try:
            a = EpicurienArticle.published.filter(issues__id=issue.id, type__slug='cote-gourmets').order_by('-publication_date')[0:1].get()
            epicurien_articles.append(a)
        except ObjectDoesNotExist:
            pass
        try:
            a = EpicurienArticle.published.filter(issues__id=issue.id, type__slug='cote-bar').order_by('-publication_date')[0:1].get()
            epicurien_articles.append(a)
        except ObjectDoesNotExist:
            pass
        try:
            a = EpicurienArticle.published.filter(issues__id=issue.id, type__slug='cote-fumeurs').order_by('-publication_date')[0:1].get()
            epicurien_articles.append(a)
        except ObjectDoesNotExist:
            pass
        context['epicurien_articles'] = epicurien_articles
    
    # Anger ("Coup de Gueule")
    if is_preview:
        try:
            anger_article = AngerArticle.preview.filter(issues__id=issue.id)
            anger_article = anger_article.order_by('-publication_date')
            anger_article = anger_article[0:1].get()
            context['anger_article'] = anger_article
        except ObjectDoesNotExist:
            context['anger_article'] = None
    else:
        try:
            anger_article = AngerArticle.published.filter(issues__id=issue.id)
            anger_article = anger_article.order_by('-publication_date')
            anger_article = anger_article[0:1].get()
            context['anger_article'] = anger_article
        except ObjectDoesNotExist:
            context['anger_article'] = None
    
    # Illustration of the day
    try:
        illustration = IllustrationOfTheDay.objects.filter(issues__id=issue.id)
        illustration = illustration[0:1].get()
        context['illustration'] = illustration
    except ObjectDoesNotExist:
        context['illustration'] = None

    # Video (reportage)
    try:
        video = Video.objects.filter(issues__id=issue.id)
        video = video[0:1].get()
        context['video'] = video
    except ObjectDoesNotExist:
        context['video'] = None
        
    # Tags 
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
    if len(tags) < 40:
        tagcloud = tags
    else:
        tagcloud = []
        for tag in tags:
            if tag.count > 2:
                tagcloud.append(tag)
                
    context['tagcloud'] = tagcloud
    
    return direct_to_template(request, 'front/home.html', context)

# ------------------------------------------------------------------------------
# CATEGORY
# ------------------------------------------------------------------------------
def category(request, category_slug, issue=None, is_preview=False, is_archive=False, is_ads_preview=False, extra_context=None):
    """
    Displays the given category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    # Context
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False

    # Is a ads preview
    if is_ads_preview:
        context['is_ads_preview'] = True
    else:
        context['is_ads_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive and not is_ads_preview:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current
    
    category = get_object_or_404(Category, slug=category_slug)
    context['category'] = category
    
    # View count
    if is_current or is_archive:
        articles = Article.published.filter(issues__id=issue.id, category=category)
        for article in articles:
            article.view_count += 1
            article.save()
        notes = Note.published.filter(issues__id=issue.id, category=category)
        for note in notes:
            note.view_count += 1
            note.save()

    note_positions = IssueNotePosition.objects.filter(issue=issue, category=category)
    for note_position in note_positions:
        if note_position.position is not None:
            varname = 'note_%s' % note_position.position.id
            if is_preview:
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
    if is_preview:
        try:
            article = Article.preview.filter(issues__id=issue.id, category__slug=category_slug)
            article = article.order_by('-publication_date')
            article = article[0:1].get()
            context['article'] = article
        except ObjectDoesNotExist:
            context['article'] = None
    else:
        try:
            article = Article.published.filter(issues__id=issue.id, category__slug=category_slug)
            article = article.order_by('-publication_date')
            article = article[0:1].get()
            context['article'] = article
        except ObjectDoesNotExist:
            context['article'] = None
    
    return direct_to_template(request, 'front/category.html', context)


# ------------------------------------------------------------------------------
# REGIONS
# ------------------------------------------------------------------------------
def regions(request, issue=None, is_preview=False, is_archive=False, is_ads_preview=False, extra_context=None):
    """
    Displays "Regions" category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    # Context
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False

    # Is a ads preview
    if is_ads_preview:
        context['is_ads_preview'] = True
    else:
        context['is_ads_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive and not is_ads_preview:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current
        
    # View count
    if is_current or is_archive:
        notes = RegionNote.published.filter(issues__id=issue.id)
        for note in notes:
            note.view_count += 1
            note.save()
    
    # Featured region
    try:
        featured_region = FeaturedRegion.objects.get(issue=issue)
    except ObjectDoesNotExist:
        featured_region = None
    
    # Featured region note
    if featured_region:
        if is_preview:
            try:
                featured_region_note = RegionNote.preview.filter(issues__id=issue.id, region=featured_region.region).order_by('-publication_date')[0:1].get()
                context['featured_region_note'] = featured_region_note
            except ObjectDoesNotExist:
                context['featured_region_note'] = None
        else:
            try:
                featured_region_note = RegionNote.published.filter(issues__id=issue.id, region=featured_region.region).order_by('-publication_date')[0:1].get()
                context['featured_region_note'] = featured_region_note
            except ObjectDoesNotExist:
                context['featured_region_note'] = None
    
    # Regions notes
    if is_preview:
        try:
            regions_notes = RegionNote.preview.filter(issues__id=issue.id).order_by('region__name')
            regions_notes = regions_notes.exclude(id=featured_region_note.id)
            context['regions_notes_1'] = regions_notes[0:10]
            context['regions_notes_2'] = regions_notes[10:20]
            context['regions_notes_3'] = regions_notes[20:]
        except ObjectDoesNotExist:
            context['regions_notes_1'] = None
            context['regions_notes_2'] = None
            context['regions_notes_3'] = None
    else:
        try:
            regions_notes = RegionNote.published.filter(issues__id=issue.id).order_by('region__name')
            regions_notes = regions_notes.exclude(id=featured_region_note.id)
            context['regions_notes_1'] = regions_notes[0:10]
            context['regions_notes_2'] = regions_notes[10:20]
            context['regions_notes_3'] = regions_notes[20:]
        except ObjectDoesNotExist:
            context['regions_notes_1'] = None
            context['regions_notes_2'] = None
            context['regions_notes_3'] = None
    
    return direct_to_template(request, 'front/regions.html', context)


# ------------------------------------------------------------------------------
# VOYAGES
# ------------------------------------------------------------------------------
def voyages(request, issue=None, is_preview=False, is_archive=False, is_ads_preview=False, extra_context=None):
    """
    Displays "Voyages" category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    # Context
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False

    # Is a ads preview
    if is_ads_preview:
        context['is_ads_preview'] = True
    else:
        context['is_ads_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive and not is_ads_preview:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current
    
    # View count
    if is_current or is_archive:
        articles = VoyagesArticle.published.filter(issues__id=issue.id)
        for article in articles:
            article.view_count += 1
            article.save()    
    
    if is_preview:
        try:
            article = VoyagesArticle.preview.filter(issues__id=issue.id)
            article = article.order_by('-publication_date')
            article = article[0:1].get()
            context['article'] = article
        except ObjectDoesNotExist:
            article = None
            context['article'] = article
    else:
        try:
            article = VoyagesArticle.published.filter(issues__id=issue.id)
            article = article.order_by('-publication_date')
            article = article[0:1].get()
            context['article'] = article
        except ObjectDoesNotExist:
            article = None
            context['article'] = article
        
    if is_preview:
        try:
            archives = VoyagesArticle.preview.all()
            if hasattr(article, 'id'):
                archives = archives.exclude(id=article.id)
            archives = archives.order_by('-publication_date')[:10]
            context['archives'] = archives
        except IndexError:
            archives = None
            context['archives'] = archives
        except ObjectDoesNotExist:
            archives = None
            context['archives'] = archives
    else:
        try:
            archives = VoyagesArticle.published.all()
            archives = archives.exclude(id=article.id)
            archives = archives.order_by('-publication_date')[:10]
            context['archives'] = archives
        except IndexError:
            archives = None
            context['archives'] = archives
        except ObjectDoesNotExist:
            archives = None
            context['archives'] = archives
        
    return direct_to_template(request, 'front/voyages.html', context)


# ------------------------------------------------------------------------------
# EPICURIEN
# ------------------------------------------------------------------------------
def epicurien(request, issue=None, is_preview=False, is_archive=False, is_ads_preview=False, extra_context=None):
    """
    Displays "Epicurien" category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    # Context
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False

    # Is a ads preview
    if is_ads_preview:
        context['is_ads_preview'] = True
    else:
        context['is_ads_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive and not is_ads_preview:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current
        
    # View count
    if is_current or is_archive:
        epicurien_articles = EpicurienArticle.published.filter(issues__id=issue.id)
        for article in epicurien_articles:
            article.view_count += 1
            article.save()
    
    # Types
    type_cotefumeurs  = EpicurienArticleType.objects.get(slug='cote-fumeurs')
    type_cotegourmets = EpicurienArticleType.objects.get(slug='cote-gourmets')
    type_cotebar      = EpicurienArticleType.objects.get(slug='cote-bar')
    
    # Côté fumeurs
    if is_preview:
        try:
            article_cotefumeurs = EpicurienArticle.preview.filter(issues__id=issue.id, type=type_cotefumeurs)
            article_cotefumeurs = article_cotefumeurs.order_by('-publication_date')
            article_cotefumeurs = article_cotefumeurs[0:1].get()
            context['article_cotefumeurs'] = article_cotefumeurs
        except ObjectDoesNotExist:
            article_cotefumeurs = None
            context['article_cotefumeurs'] = article_cotefumeurs
    else:
        try:
            article_cotefumeurs = EpicurienArticle.published.filter(issues__id=issue.id, type=type_cotefumeurs)
            article_cotefumeurs = article_cotefumeurs.order_by('-publication_date')
            article_cotefumeurs = article_cotefumeurs[0:1].get()
            context['article_cotefumeurs'] = article_cotefumeurs
        except ObjectDoesNotExist:
            article_cotefumeurs = None
            context['article_cotefumeurs'] = article_cotefumeurs
    
    if is_preview:
        try:
            archives_cotefumeurs = EpicurienArticle.preview.filter(type=type_cotefumeurs)
            if hasattr(article_cotefumeurs, 'id'):
                archives_cotefumeurs = archives_cotefumeurs.exclude(id=article_cotefumeurs.id)
            archives_cotefumeurs = archives_cotefumeurs.order_by('-publication_date')[:10]
            context['archives_cotefumeurs'] = archives_cotefumeurs
        except IndexError:
            archives_cotefumeurs = None
            context['archives_cotefumeurs'] = archives_cotefumeurs
        except ObjectDoesNotExist:
            archives_cotefumeurs = None
            context['archives_cotefumeurs'] = archives_cotefumeurs
    else:
        try:
            archives_cotefumeurs = EpicurienArticle.published.filter(type=type_cotefumeurs)
            archives_cotefumeurs = archives_cotefumeurs.exclude(id=article_cotefumeurs.id)
            archives_cotefumeurs = archives_cotefumeurs.order_by('-publication_date')[:10]
            context['archives_cotefumeurs'] = archives_cotefumeurs
        except ObjectDoesNotExist:
            archives_cotefumeurs = None
            context['archives_cotefumeurs'] = archives_cotefumeurs
    
    # Côté Gourmets
    if is_preview:
        try:
            article_cotegourmets =  EpicurienArticle.preview.filter(issues__id=issue.id, type=type_cotegourmets)
            article_cotegourmets = article_cotegourmets.order_by('-publication_date')
            article_cotegourmets = article_cotegourmets[0:1].get()
            context['article_cotegourmets'] = article_cotegourmets
        except ObjectDoesNotExist:
            article_cotegourmets = None
            context['article_cotegourmets'] = article_cotegourmets
    else:
        try:
            article_cotegourmets = EpicurienArticle.published.filter(issues__id=issue.id, type=type_cotegourmets)
            article_cotegourmets = article_cotegourmets.order_by('-publication_date')
            article_cotegourmets = article_cotegourmets[0:1].get()
            context['article_cotegourmets'] = article_cotegourmets
        except ObjectDoesNotExist:
            article_cotegourmets = None
            context['article_cotegourmets'] = article_cotegourmets
    
    if is_preview:
        try:
            archives_cotegourmets = EpicurienArticle.preview.filter(type=type_cotegourmets)
            if hasattr(article_cotegourmets, 'id'):
                archives_cotegourmets = archives_cotegourmets.exclude(id=article_cotegourmets.id)
            archives_cotegourmets = archives_cotegourmets.order_by('-publication_date')[:10]
            context['archives_cotegourmets'] = archives_cotegourmets
        except ObjectDoesNotExist:
            archives_cotegourmets = None
            context['archives_cotegourmets'] = archives_cotegourmets
    else:
        try:
            archives_cotegourmets = EpicurienArticle.published.filter(type=type_cotegourmets)
            archives_cotegourmets = archives_cotegourmets.exclude(id=article_cotegourmets.id)
            archives_cotegourmets = archives_cotegourmets.order_by('-publication_date')[:10]
            context['archives_cotegourmets'] = archives_cotegourmets
        except ObjectDoesNotExist:
            archives_cotegourmets = None
            context['archives_cotegourmets'] = archives_cotegourmets
    
    # Côté Bar
    if is_preview:
        try:
            article_cotebar = EpicurienArticle.preview.filter(issues__id=issue.id, type=type_cotebar)
            article_cotebar = article_cotebar.order_by('-publication_date')
            article_cotebar = article_cotebar[0:1].get()
            context['article_cotebar'] = article_cotebar
        except ObjectDoesNotExist:
            article_cotebar = None
            context['article_cotebar'] = article_cotebar
    else:
        try:
            article_cotebar = EpicurienArticle.published.filter(issues__id=issue.id, type=type_cotebar)
            article_cotebar = article_cotebar.order_by('-publication_date')
            article_cotebar = article_cotebar[0:1].get()
            context['article_cotebar'] = article_cotebar
        except ObjectDoesNotExist:
            article_cotebar = None
            context['article_cotebar'] = article_cotebar
    
    if is_preview:
        try:
            archives_cotebar = EpicurienArticle.preview.filter(type=type_cotebar).order_by('-publication_date')
            if hasattr(article_cotebar, 'id'):
                archives_cotebar = archives_cotebar.exclude(id=article_cotebar.id)
            archives_cotebar = archives_cotebar.order_by('-publication_date')[:10]
            context['archives_cotebar'] = archives_cotebar
        except ObjectDoesNotExist:
            archives_cotebar = None
            context['archives_cotebar'] = archives_cotebar
    else:
        try:
            archives_cotebar = EpicurienArticle.published.filter(type=type_cotebar)
            archives_cotebar = archives_cotebar.exclude(id=article_cotebar.id)
            archives_cotebar = archives_cotebar.order_by('-publication_date')[:10]
            context['archives_cotebar'] = archives_cotebar
        except ObjectDoesNotExist:
            archives_cotebar = None
            context['archives_cotebar'] = archives_cotebar

    return direct_to_template(request, 'front/epicurien.html', context)


# ------------------------------------------------------------------------------
# ANGER
# ------------------------------------------------------------------------------
def anger(request, issue=None, is_preview=False, is_archive=False, is_ads_preview=False, extra_context=None):
    """
    Displays "Anger" (Coup de Gueule) category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    # Context
    context = {}
    if extra_context:
        context.update(extra_context)
        
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is a ads preview
    if is_ads_preview:
        context['is_ads_preview'] = True
    else:
        context['is_ads_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive and not is_ads_preview:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current
    
    # View count
    if is_current or is_archive:
        articles = AngerArticle.published.filter(issues__id=issue.id)
        for article in articles:
            article.view_count += 1
            article.save()
    
    if is_preview:
        try:
            article = AngerArticle.preview.filter(issues__id=issue.id)
            article = article.order_by('-publication_date')
            article = article[0:1].get()
            context['article'] = article
        except ObjectDoesNotExist:
            article = None
            context['article'] = article
    else:
        try:
            article = AngerArticle.published.filter(issues__id=issue.id)
            article = article.order_by('-publication_date')
            article = article[0:1].get()
            context['article'] = article
        except ObjectDoesNotExist:
            article = None
            context['article'] = article
    
    if is_preview:
        try:
            archives = AngerArticle.preview.all()
            if hasattr(article, 'id'):
                archives = archives.exclude(id=article.id)
            archives = archives.order_by('-publication_date')[:10]
            context['archives'] = archives
        except ObjectDoesNotExist:
            archives = None
            context['archives'] = archives
    else:
        try:
            archives = AngerArticle.published.all()
            archives = archives.exclude(id=article.id)
            archives = archives.order_by('-publication_date')[:10]
            context['archives'] = archives
        except ObjectDoesNotExist:
            archives = None
            context['archives'] = archives
        
    return direct_to_template(request, 'front/anger.html', context)


