# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.front`` application.

"""
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from critica.apps.categories.models import Category
from critica.apps.issues.models import Issue
from critica.apps.positions.models import IssueCategoryPosition, IssueNotePosition
from critica.apps.articles.models import Article
from critica.apps.epicurien.models import EpicurienArticle, EpicurienArticleType
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.anger.models import AngerArticle
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote, FeaturedRegion
from critica.apps.illustrations.models import IllustrationOfTheDay
from critica.apps.videos.models import Video
from critica.apps.pages.models import Page
from critica.apps.ads.models import AdBannerPosition, AdBanner, AdCarouselPosition, AdCarousel
from critica.apps.utils import urlbase64

from tagging.models import Tag, TaggedItem
from tagging.utils import calculate_cloud


# Issue getters
# ------------------------------------------------------------------------------
def _get_current_issue(issue_number=None):
    """
    Gets the current issue (object).
    
    If parameter ``issue_number`` is defined, returns the issue object or 404
    if it does not exist. If parameter ``issue_number`` is not defined, returns
    the latest published issue object or 404 if there's no issue yet. 
    
    """
    if issue_number:
        try:
            issue = Issue.objects.get(number=issue_number)
        except ObjectDoesNotExist:
            raise Http404
    else:
        try:
            issue = Issue.objects.filter(is_published=True).order_by('-number')[0]
        except IndexError:
            raise Http404
        except ObjectDoesNotExist:
            raise Http404
    return issue



def _get_encoded_issue(issue_key):
    """
    Gets issue number from issue key and returns ``_get_current_issue()``.
    
    """
    issue_number = int(urlbase64.uri_b64decode(str(issue_key)))
    return _get_current_issue(issue_number=issue_number)



# Home and categories
# ------------------------------------------------------------------------------
def home(request, issue=None, is_preview=False, is_archive=False):
    """
    Displays the homepage.
    
    """
    # Gets the current issue
    if issue is None:
        issue = _get_current_issue()
    
    # Initializes context dictionary
    context = {}
    
    # Issue
    try:
        context['issue'] = issue
    except ObjectDoesNotExist:
        raise Htt404
        
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive:
        is_current = True
        context['is_current'] = is_current
    else:
        is_current = False
        context['is_current'] = is_current

    # Generic articles
    category_positions = IssueCategoryPosition.objects.filter(issue=issue)
    for category_position in category_positions:
        if category_position.position is not None:
            varname = 'article_%s' % category_position.position.id
            if is_preview:
                try:
                    article = Article.preview.get(issues__id=issue.id, category=category_position.category)
                    context[varname] = article
                except MultipleObjectsReturned:
                    article = Article.preview.filter(issues__id=issue.id, category=category_position.category)[0]
                    context[varname] = article
                except ObjectDoesNotExist:
                    context[varname] = None
            else:  
                try:
                    article = Article.published.get(issues__id=issue.id, category=category_position.category)
                    context[varname] = article
                except MultipleObjectsReturned:
                    article = Article.published.filter(issues__id=issue.id, category=category_position.category)[0]
                    context[varname] = article
                except ObjectDoesNotExist:
                    context[varname] = None

    # Regions
    if is_preview:
        try:
            featured = FeaturedRegion.objects.get(issue=issue)
            context['region_note'] = RegionNote.preview.get(issues__id=issue.id, region=featured.region)
        except MultipleObjectsReturned:
            context['region_note'] = RegionNote.preview.filter(issues__id=issue.id, region=featured.region)[0]
        except ObjectDoesNotExist:
            context['region_note'] = None
    else:
        try:
            featured = FeaturedRegion.objects.get(issue=issue)
            context['region_note'] = RegionNote.published.get(issues__id=issue.id, region=featured.region)
        except MultipleObjectsReturned:
            context['region_note'] = RegionNote.published.filter(issues__id=issue.id, region=featured.region)[0]
        except ObjectDoesNotExist:
            context['region_note'] = None

    # Voyages
    if is_preview:
        try:
            context['voyages_article'] = VoyagesArticle.preview.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['voyages_article'] = VoyagesArticle.preview.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['voyages_article'] = None
    else:
        try:
            context['voyages_article'] = VoyagesArticle.published.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['voyages_article'] = VoyagesArticle.published.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['voyages_article'] = None
    
    # Epicurien
    if is_preview:
        try:
            context['epicurien_articles'] = EpicurienArticle.preview.filter(issues__id=issue.id)
        except ObjectDoesNotExist:
            context['epicurien_articles'] = None
    else:
        try:
            context['epicurien_articles'] = EpicurienArticle.published.filter(issues__id=issue.id)
        except ObjectDoesNotExist:
            context['epicurien_articles'] = None
    
    # Anger ("Coup de Gueule")
    if is_preview:
        try:
            context['anger_article'] = AngerArticle.preview.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['anger_article'] = AngerArticle.preview.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['anger_article'] = None
    else:
        try:
            context['anger_article'] = AngerArticle.published.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['anger_article'] = AngerArticle.published.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['anger_article'] = None
    
    # Illustration of the day
    try:
        context['illustration'] = IllustrationOfTheDay.objects.get(issues__id=issue.id)
    except MultipleObjectsReturned:
        context['illustration'] = IllustrationOfTheDay.objects.filter(issues__id=issue.id)[0]
    except ObjectDoesNotExist:
        context['illustration'] = None

    # Video (reportage)
    try:
        context['video'] = Video.objects.get(issues__id=issue.id)
    except MultipleObjectsReturned:
        context['video'] = Video.objects.filter(issues__id=issue.id)[0]
    except ObjectDoesNotExist:
        context['video'] = None
        
    # Tags 
    all_tags = []
    article_tags = Tag.objects.usage_for_model(Article, counts=True)
    for tag in article_tags:
        all_tags.append(tag)
        
    note_tags = Tag.objects.usage_for_model(Note, counts=True)
    for tag in note_tags:
        all_tags.append(tag)
    
    region_tags = Tag.objects.usage_for_model(RegionNote, counts=True)
    for tag in region_tags:
        all_tags.append(tag)
        
    voyages_tags = Tag.objects.usage_for_model(VoyagesArticle, counts=True)
    for tag in voyages_tags:
        all_tags.append(tag)
        
    epicurien_tags = Tag.objects.usage_for_model(VoyagesArticle, counts=True)
    for tag in epicurien_tags:
        all_tags.append(tag)
        
    anger_tags = Tag.objects.usage_for_model(AngerArticle, counts=True)
    for tag in anger_tags:
        all_tags.append(tag)
        
    tags = calculate_cloud(all_tags, steps=10)
    tagcloud = []
    for tag in tags:
        if tag.font_size > 2:
            tagcloud.append(tag)
    context['tagcloud'] = tagcloud
    
    return render_to_response(
        'front/home.html', 
        context, 
        context_instance=RequestContext(request))



def category(request, category_slug, issue=None, is_preview=False, is_archive=False):
    """
    Displays the given category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    context = {}
    
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive:
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
                    note = Note.preview.get(issues__id=issue.id, type=note_position.type, category=category)
                    context[varname] = note
                except MultipleObjectsReturned:
                    note = Note.preview.filter(issues__id=issue.id, type=note_position.type, category=category)[0]
                    context[varname] = note
                except ObjectDoesNotExist:
                    context[varname] = None
            else:
                try:
                    note = Note.published.get(issues__id=issue.id, type=note_position.type, category=category)
                    context[varname] = note
                except MultipleObjectsReturned:
                    note = Note.published.filter(issues__id=issue.id, type=note_position.type, category=category)[0]
                    context[varname] = note
                except ObjectDoesNotExist:
                    context[varname] = None
    if is_preview:
        try:
            context['article'] = Article.preview.get(issues__id=issue.id, category__slug=category_slug)
        except MultipleObjectsReturned:
            context['article'] = Article.preview.filter(issues__id=issue.id, category__slug=category_slug)[0]
        except ObjectDoesNotExist:
            context['article'] = None
    else:
        try:
            context['article'] = Article.published.get(issues__id=issue.id, category__slug=category_slug)
        except MultipleObjectsReturned:
            context['article'] = Article.published.filter(issues__id=issue.id, category__slug=category_slug)[0]
        except ObjectDoesNotExist:
            context['article'] = None
    
    return render_to_response(
        'front/category.html', 
        context, 
        context_instance=RequestContext(request))



def regions(request, issue=None, is_preview=False, is_archive=False):
    """
    Displays "Regions" category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    context = {}
    
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive:
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
        try:
            featured_region_note = RegionNote.preview.get(issues__id=issue.id, region=featured_region.region)
            context['featured_region_note'] = featured_region_note
        except MultipleObjectsReturned:
            featured_region_note = RegionNote.preview.filter(issues__id=issue.id, region=featured_region.region)[0]
            context['featured_region_note'] = featured_region_note
        except ObjectDoesNotExist:
            context['featured_region_note'] = None
    else:
        context['featured_region_note'] = None
    
    # Regions notes
    if is_preview:
        try:
            regions_notes = RegionNote.preview.filter(issues__id=issue.id)
            if featured_region:
                regions_notes.exclude(id=featured_region.id)
            regions_notes.order_by('region__name')
            context['regions_notes_1'] = regions_notes[0:10]
            context['regions_notes_2'] = regions_notes[10:20]
            context['regions_notes_3'] = regions_notes[20:]
        except ObjectDoesNotExist:
            context['regions_notes_1'] = None
            context['regions_notes_2'] = None
            context['regions_notes_3'] = None
    else:
        try:
            regions_notes = RegionNote.published.filter(issues__id=issue.id)
            if featured_region:
                regions_notes.exclude(id=featured_region.id)
            regions_notes.order_by('region__name')
            context['regions_notes_1'] = regions_notes[0:10]
            context['regions_notes_2'] = regions_notes[10:20]
            context['regions_notes_3'] = regions_notes[20:]
        except ObjectDoesNotExist:
            context['regions_notes_1'] = None
            context['regions_notes_2'] = None
            context['regions_notes_3'] = None
    
    return render_to_response(
        'front/regions.html',
        context,
        context_instance=RequestContext(request))



def voyages(request, issue=None, is_preview=False, is_archive=False):
    """
    Displays "Voyages" category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    context = {}
    
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive:
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
            context['article'] = VoyagesArticle.preview.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['article'] = VoyagesArticle.preview.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['article'] = None
    else:
        try:
            context['article'] = VoyagesArticle.published.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['article'] = VoyagesArticle.published.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['article'] = None
        
    if is_preview:
        try:
            context['archives'] = VoyagesArticle.preview.order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives'] = None
    else:
        try:
            context['archives'] = VoyagesArticle.published.order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives'] = None
        
    return render_to_response(
        'front/voyages.html', 
        context, 
        context_instance=RequestContext(request))



def epicurien(request, issue=None, is_preview=False, is_archive=False):
    """
    Displays "Epicurien" category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    context = {}
    
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive:
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
            context['article_cotefumeurs'] = EpicurienArticle.preview.get(issues__id=issue.id, type=type_cotefumeurs)
        except MultipleObjectsReturned:
            context['article_cotefumeurs'] = EpicurienArticle.preview.filter(issues__id=issue.id, type=type_cotefumeurs)[0]
        except ObjectDoesNotExist:
            context['article_cotefumeurs'] = None
    else:
        try:
            context['article_cotefumeurs'] = EpicurienArticle.published.get(issues__id=issue.id, type=type_cotefumeurs)
        except MultipleObjectsReturned:
            context['article_cotefumeurs'] = EpicurienArticle.published.filter(issues__id=issue.id, type=type_cotefumeurs)[0]
        except ObjectDoesNotExist:
            context['article_cotefumeurs'] = None
    
    if is_preview:
        try:
            context['archives_cotefumeurs'] = EpicurienArticle.preview.filter(type=type_cotefumeurs).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotefumeurs'] = None
    else:
        try:
            context['archives_cotefumeurs'] = EpicurienArticle.published.filter(type=type_cotefumeurs).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotefumeurs'] = None
    
    # Côté Gourmets
    if is_preview:
        try:
            context['article_cotegourmets'] = EpicurienArticle.preview.get(issues__id=issue.id, type=type_cotegourmets)
        except MultipleObjectsReturned:
            context['article_cotegourmets'] = EpicurienArticle.preview.filter(issues__id=issue.id, type=type_cotegourmets)[0]
        except ObjectDoesNotExist:
            context['article_cotegourmets'] = None
    else:
        try:
            context['article_cotegourmets'] = EpicurienArticle.published.get(issues__id=issue.id, type=type_cotegourmets)
        except MultipleObjectsReturned:
            context['article_cotegourmets'] = EpicurienArticle.published.filter(issues__id=issue.id, type=type_cotegourmets)[0]
        except ObjectDoesNotExist:
            context['article_cotegourmets'] = None
    
    if is_preview:
        try:
            context['archives_cotegourmets'] = EpicurienArticle.preview.filter(type=type_cotegourmets).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotegourmets'] = None
    else:
        try:
            context['archives_cotegourmets'] = EpicurienArticle.published.filter(type=type_cotegourmets).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotegourmets'] = None
    
    # Côté Bar
    if is_preview:
        try:
            context['article_cotebar'] = EpicurienArticle.preview.get(issues__id=issue.id, type=type_cotebar)
        except MultipleObjectsReturned:
            context['article_cotebar'] = EpicurienArticle.preview.filter(issues__id=issue.id, type=type_cotebar)[0]
        except ObjectDoesNotExist:
            context['article_cotebar'] = None
    else:
        try:
            context['article_cotebar'] = EpicurienArticle.published.get(issues__id=issue.id, type=type_cotebar)
        except MultipleObjectsReturned:
            context['article_cotebar'] = EpicurienArticle.published.filter(issues__id=issue.id, type=type_cotebar)[0]
        except ObjectDoesNotExist:
            context['article_cotebar'] = None
    
    if is_preview:
        try:
            context['archives_cotebar'] = EpicurienArticle.preview.filter(type=type_cotebar).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotebar'] = None
    else:
        try:
            context['archives_cotebar'] = EpicurienArticle.published.filter(type=type_cotebar).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotebar'] = None

    return render_to_response(
        'front/epicurien.html', 
        context, 
        context_instance=RequestContext(request))



def anger(request, issue=None, is_preview=False, is_archive=False):
    """
    Displays "Anger" (Coup de Gueule) category page.
    
    """
    if not issue:
        issue = _get_current_issue()
    
    context = {}
    
    # Issue
    context['issue'] = issue
    
    # Is a preview
    if is_preview:
        context['is_preview'] = True
    else:
        context['is_preview'] = False
        
    # Is an archive
    if is_archive:
        context['is_archive'] = True
    else:
        context['is_archive'] = False
        
    # Is current
    if not is_preview and not is_archive:
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
            context['article'] = AngerArticle.preview.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['article'] = AngerArticle.preview.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['article'] = None
    else:
        try:
            context['article'] = AngerArticle.published.get(issues__id=issue.id)
        except MultipleObjectsReturned:
            context['article'] = AngerArticle.published.filter(issues__id=issue.id)[0]
        except ObjectDoesNotExist:
            context['article'] = None
    
    if is_preview:
        try:
            context['archives'] = AngerArticle.preview.order_by('-publication_date')
        except ObjectDoesNotExist:
            context['archives'] = None
    else:
        try:
            context['archives'] = AngerArticle.published.order_by('-publication_date')
        except ObjectDoesNotExist:
            context['archives'] = None
        
    return render_to_response(
        'front/anger.html', 
        context, 
        context_instance=RequestContext(request))



# Issue archive
# ------------------------------------------------------------------------------
def archives(request):
    """
    Displays archive list.
    
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
        
    return render_to_response(
        'front/archives.html', 
        context, 
        context_instance=RequestContext(request)
    )



def issuearchive_home(request, issue_number):
    """
    Displays home archive of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return home(request, issue=issue, is_archive=True)



def issuearchive_category(request, issue_number, category_slug):
    """
    Displays category archive of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return category(request, category_slug, issue=issue, is_archive=True)



def issuearchive_regions(request, issue_number):
    """
    Displays "Regions" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return regions(request, issue=issue, is_archive=True)



def issuearchive_voyages(request, issue_number):
    """
    Displays "Voyages" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return voyages(request, issue=issue, is_archive=True)



def issuearchive_epicurien(request, issue_number):
    """
    Displays "Epicurien" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return epicurien(request, issue=issue, is_archive=True)



def issuearchive_anger(request, issue_number):
    """
    Displays "Anger" category of a given issue.
    
    """
    issue = _get_current_issue(issue_number=issue_number)
    return anger(request, issue=issue, is_archive=True)



# Issue preview
# ------------------------------------------------------------------------------
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



# Tags
# ------------------------------------------------------------------------------
def tags(request):
    """
    Displays all tags as tag cloud.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    all_tags = []
    article_tags = Tag.objects.usage_for_model(Article, counts=True)
    for tag in article_tags:
        all_tags.append(tag)
        
    note_tags = Tag.objects.usage_for_model(Note, counts=True)
    for tag in note_tags:
        all_tags.append(tag)
    
    region_tags = Tag.objects.usage_for_model(RegionNote, counts=True)
    for tag in region_tags:
        all_tags.append(tag)
        
    voyages_tags = Tag.objects.usage_for_model(VoyagesArticle, counts=True)
    for tag in voyages_tags:
        all_tags.append(tag)
        
    epicurien_tags = Tag.objects.usage_for_model(VoyagesArticle, counts=True)
    for tag in epicurien_tags:
        all_tags.append(tag)
        
    anger_tags = Tag.objects.usage_for_model(AngerArticle, counts=True)
    for tag in anger_tags:
        all_tags.append(tag)
        
    context['tags'] = calculate_cloud(all_tags, steps=10)
    
    return render_to_response(
        'front/tags.html', 
        context, 
        context_instance=RequestContext(request))


    
def tags_tag(request, tag):
    """
    Displays articles / notes tagged with a given tag.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    tag = get_object_or_404(Tag, name=tag)
    context['tag'] = tag
        
    items = []
    
    articles = TaggedItem.objects.get_by_model(Article.published.order_by('-publication_date'), tag)
    if articles:
        for article in articles:
            items.append((article.id, article))
    
    notes = TaggedItem.objects.get_by_model(Note.published.order_by('-publication_date'), tag)
    if notes:
        for note in notes:
            items.append((note.id, note))
        
    regions = TaggedItem.objects.get_by_model(RegionNote.published.order_by('-publication_date'), tag)
    if regions:
        for region in regions:
            items.append((region.id, region))
            
    voyages = TaggedItem.objects.get_by_model(VoyagesArticle.published.order_by('-publication_date'), tag)
    if voyages:
        for voyage in voyages:
            items.append((voyage.id, voyage))
            
    epicurien = TaggedItem.objects.get_by_model(EpicurienArticle.published.order_by('-publication_date'), tag)
    if epicurien:
        for e in epicurien:
            items.append((e.id, e))
            
    anger = TaggedItem.objects.get_by_model(AngerArticle.published.order_by('-publication_date'), tag)
    if anger:
        for a in anger:
            items.append((a.id, a))
    
    item_list = [item for k, item in items]
    
    # Pagination
    paginator = Paginator(item_list, 30)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        context['items'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        context['items'] = paginator.page(paginator.num_pages)

    return render_to_response(
        'front/tags_tag.html', 
        context, 
        context_instance=RequestContext(request))



# Search
# ------------------------------------------------------------------------------
def search(request):
    """
    Displays search results.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    if request.method == 'POST':
        search_item = request.POST['search']
        context['search_item'] = search_item
        
        items = []
        from django.db.models import Q
        
        articles = Article.objects.filter(
            Q(title__icontains=search_item) | 
            Q(summary__icontains=search_item) | 
            Q(content__icontains=search_item) |
            Q(tags__icontains=search_item) & 
            Q(is_ready_to_publish=True, is_reserved=False)).order_by('-publication_date')
        if articles:
            for article in articles:
                items.append((article.id, article))
        
        notes = Note.objects.filter(
            Q(title__icontains=search_item) | 
            Q(content__icontains=search_item) |
            Q(tags__icontains=search_item) & 
            Q(is_ready_to_publish=True, is_reserved=False)).order_by('-publication_date')
        if notes:
            for note in notes:
                items.append((note.id, note))
            
        regions = RegionNote.objects.filter(
            Q(title__icontains=search_item) | 
            Q(content__icontains=search_item) |
            Q(tags__icontains=search_item) & 
            Q(is_ready_to_publish=True, is_reserved=False)).order_by('-publication_date')
        if regions:
            for region in regions:
                items.append((region.id, region))
                
        voyages = VoyagesArticle.objects.filter(
            Q(title__icontains=search_item) | 
            Q(summary__icontains=search_item) | 
            Q(content__icontains=search_item) |
            Q(tags__icontains=search_item) & 
            Q(is_ready_to_publish=True, is_reserved=False)).order_by('-publication_date')
        if voyages:
            for voyage in voyages:
                items.append((voyage.id, voyage))
                
        epicurien = EpicurienArticle.objects.filter(
            Q(title__icontains=search_item) | 
            Q(summary__icontains=search_item) | 
            Q(content__icontains=search_item) |
            Q(tags__icontains=search_item) & 
            Q(is_ready_to_publish=True, is_reserved=False)).order_by('-publication_date')
        if epicurien:
            for e in epicurien:
                items.append((e.id, e))
                
        anger = AngerArticle.objects.filter(
            Q(title__icontains=search_item) | 
            Q(summary__icontains=search_item) | 
            Q(content__icontains=search_item) |
            Q(tags__icontains=search_item) & 
            Q(is_ready_to_publish=True, is_reserved=False)).order_by('-publication_date')
        if anger:
            for a in anger:
                items.append((a.id, a))
        
        item_list = [item for k, item in items]
        
        # Pagination
        paginator = Paginator(item_list, 30)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            context['items'] = paginator.page(page)
        except (EmptyPage, InvalidPage):
            context['items'] = paginator.page(paginator.num_pages)
    else:
        return HttpResponseRedirect('/')
        
    return render_to_response(
        'front/search_results.html',
        context,
        context_instance=RequestContext(request)
    )


# RSS
# ------------------------------------------------------------------------------
def rss_index(request):
    """
    Displays RSS index page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    try:
        context['categories'] = Category.objects.all()
    except ObjectDoesNotExist:
        context['categories'] = False
        
    return render_to_response(
        'front/rss_index.html', 
        context, 
        context_instance=RequestContext(request))


# Pages
# ------------------------------------------------------------------------------
def page_legal(request):
    """
    Displays the legal page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    context['page'] = get_object_or_404(Page.objects.all(), slug='mentions-legales', is_published=True)
    
    return render_to_response(
        'front/page.html', 
        context, 
        context_instance=RequestContext(request))


def page_ads(request):
    """
    Displays the ad page.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    context['page'] = get_object_or_404(Page.objects.all(), slug='publicites', is_published=True)
    
    return render_to_response(
        'front/page.html', 
        context, 
        context_instance=RequestContext(request))


