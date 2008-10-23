# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.front`` application.

"""
from django.conf import settings
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage
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
from critica.apps.pages.models import Page
from critica.apps.ads.models import AdBannerPosition
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarouselPosition
from critica.apps.ads.models import AdCarousel
from critica.apps.utils import urlbase64
from tagging.models import Tag
from tagging.models import TaggedItem
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
        context['is_current'] = True
    else:
        context['is_current'] = False

    # Generic articles
    category_positions = IssueCategoryPosition.objects.filter(issue=issue)
    for category_position in category_positions:
        if category_position.position is not None:
            varname = 'article_%s' % category_position.position.id
            if is_preview:
                try:
                    article = Article.objects.get(
                    issues__id=issue.id,  
                    is_reserved=False, 
                    category=category_position.category)
                    context[varname] = article
                except MultipleObjectsReturned:
                    article = Article.objects.filter(
                    issues__id=issue.id,  
                    is_reserved=False, 
                    category=category_position.category)[0]
                    context[varname] = article
                except ObjectDoesNotExist:
                    context[varname] = False
            else:  
                try:
                    article = Article.objects.get(
                    issues__id=issue.id, 
                    is_ready_to_publish=True, 
                    is_reserved=False, 
                    category=category_position.category)
                    context[varname] = article
                except MultipleObjectsReturned:
                    article = Article.objects.filter(
                    issues__id=issue.id, 
                    is_ready_to_publish=True, 
                    is_reserved=False, 
                    category=category_position.category)[0]
                    context[varname] = article
                except ObjectDoesNotExist:
                    context[varname] = False

    # Regions
    if is_preview:
        try:
            featured = FeaturedRegion.objects.get(issue=issue)
            context['region_note'] = RegionNote.objects.get(
                issues__id=issue.id,  
                is_reserved=False, 
                region=featured.region)
        except MultipleObjectsReturned:
            context['region_note'] = RegionNote.objects.filter(
                issues__id=issue.id,  
                is_reserved=False, 
                region=featured.region)[0]
        except ObjectDoesNotExist:
            context['region_note'] = False
    else:
        try:
            featured = FeaturedRegion.objects.get(issue=issue)
            context['region_note'] = RegionNote.objects.get(
                issues__id=issue.id, 
                is_ready_to_publish=True, 
                is_reserved=False, 
                region=featured.region)
        except MultipleObjectsReturned:
            context['region_note'] = RegionNote.objects.filter(
                issues__id=issue.id, 
                is_ready_to_publish=True, 
                is_reserved=False, 
                region=featured.region)[0]
        except ObjectDoesNotExist:
            context['region_note'] = False

    # Voyages
    if is_preview:
        try:
            context['voyages_article'] = VoyagesArticle.objects.get(issues__id=issue.id, is_reserved=False)
        except MultipleObjectsReturned:
            context['voyages_article'] = VoyagesArticle.objects.filter(issues__id=issue.id, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['voyages_article'] = False
    else:
        try:
            context['voyages_article'] = VoyagesArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
        except MultipleObjectsReturned:
            context['voyages_article'] = VoyagesArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['voyages_article'] = False
    
    # Epicurien
    if is_preview:
        try:
            context['epicurien_articles'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_reserved=False)
        except ObjectDoesNotExist:
            context['epicurien_articles'] = False
    else:
        try:
            context['epicurien_articles'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
        except ObjectDoesNotExist:
            context['epicurien_articles'] = False
    
    # Anger ("Coup de Gueule")
    if is_preview:
        try:
            context['anger_article'] = AngerArticle.objects.get(issues__id=issue.id, is_reserved=False)
        except MultipleObjectsReturned:
            context['anger_article'] = AngerArticle.objects.filter(issues__id=issue.id, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['anger_article'] = False
    else:
        try:
            context['anger_article'] = AngerArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
        except MultipleObjectsReturned:
            context['anger_article'] = AngerArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['anger_article'] = False
    
    # Illustration of the day
    try:
        context['illustration'] = IllustrationOfTheDay.objects.get(issues__id=issue.id)
    except MultipleObjectsReturned:
        context['illustration'] = IllustrationOfTheDay.objects.filter(issues__id=issue.id)[0]
    except ObjectDoesNotExist:
        context['illustration'] = False

    # Video (reportage)
    try:
        context['video'] = Video.objects.get(issues__id=issue.id)
    except MultipleObjectsReturned:
        context['video'] = Video.objects.filter(issues__id=issue.id)[0]
    except ObjectDoesNotExist:
        context['video'] = False
        
    # Ads
    try:
        context['ads'] = AdBannerPosition.objects.filter(page__id=1)
    except ObjectDoesNotExist:
        context['ads'] = False
        
    # Ad banners
    try:
        context['adbanners'] = AdBanner.objects.filter(positions__page__id=1)
    except ObjectDoesNotExist:
        context['adbanners'] = False
        
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
        context['is_current'] = True
    else:
        context['is_current'] = False
    
    category = get_object_or_404(Category, slug=category_slug)
    context['category'] = category

    note_positions = IssueNotePosition.objects.filter(issue=issue, category=category)
    for note_position in note_positions:
        if note_position.position is not None:
            varname = 'note_%s' % note_position.position.id
            if is_preview:
                try:
                    note = Note.objects.get(
                        issues__id=issue.id, 
                        is_reserved=False, 
                        type=note_position.type,
                        category=category)
                    context[varname] = note
                except MultipleObjectsReturned:
                    note = Note.objects.filter(
                        issues__id=issue.id,  
                        is_reserved=False, 
                        type=note_position.type,
                        category=category)[0]
                    context[varname] = note
                except ObjectDoesNotExist:
                    context[varname] = False
            else:
                try:
                    note = Note.objects.get(
                        issues__id=issue.id, 
                        is_ready_to_publish=True, 
                        is_reserved=False, 
                        type=note_position.type,
                        category=category)
                    context[varname] = note
                except MultipleObjectsReturned:
                    note = Note.objects.filter(
                        issues__id=issue.id, 
                        is_ready_to_publish=True, 
                        is_reserved=False, 
                        type=note_position.type,
                        category=category)[0]
                    context[varname] = note
                except ObjectDoesNotExist:
                    context[varname] = False
    if is_preview:
        try:
            context['article'] = Article.objects.get(issues__id=issue.id, is_reserved=False, category__slug=category_slug)
        except MultipleObjectsReturned:
            context['article'] = Article.objects.filter(issues__id=issue.id, is_reserved=False, category__slug=category_slug)[0]
        except ObjectDoesNotExist:
            context['article'] = False
    else:
        try:
            context['article'] = Article.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, category__slug=category_slug)
        except MultipleObjectsReturned:
            context['article'] = Article.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, category__slug=category_slug)[0]
        except ObjectDoesNotExist:
            context['article'] = False
    
        
    return render_to_response('front/category.html', context, context_instance=RequestContext(request))



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
        context['is_current'] = True
    else:
        context['is_current'] = False
    
    # Featured region
    try:
        featured_region = FeaturedRegion.objects.get(issue=issue)
    except ObjectDoesNotExist:
        featured_region = None
    
    # Featured region note
    if featured_region:
        try:
            featured_region_note = RegionNote.objects.get(issues__id=issue.id, is_reserved=False, region=featured_region.region)
            context['featured_region_note'] = featured_region_note
        except MultipleObjectsReturned:
            featured_region_note = RegionNote.objects.filter(issues__id=issue.id, is_reserved=False, region=featured_region.region)[0]
            context['featured_region_note'] = featured_region_note
        except ObjectDoesNotExist:
            context['featured_region_note'] = False
    else:
        context['featured_region_note'] = False
    
    # Regions notes
    if is_preview:
        try:
            regions_notes = RegionNote.objects.filter(issues__id=issue.id, is_reserved=False)
            if featured_region:
                regions_notes.exclude(id=featured_region.id)
            regions_notes.order_by('region__name')
            context['regions_notes_1'] = regions_notes[0:10]
            context['regions_notes_2'] = regions_notes[10:20]
            context['regions_notes_3'] = regions_notes[20:]
        except ObjectDoesNotExist:
            context['regions_notes_1'] = False
            context['regions_notes_2'] = False
            context['regions_notes_3'] = False
    else:
        try:
            regions_notes = RegionNote.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
            if featured_region:
                regions_notes.exclude(id=featured_region.id)
            regions_notes.order_by('region__name')
            context['regions_notes_1'] = regions_notes[0:10]
            context['regions_notes_2'] = regions_notes[10:20]
            context['regions_notes_3'] = regions_notes[20:]
        except ObjectDoesNotExist:
            context['regions_notes_1'] = False
            context['regions_notes_2'] = False
            context['regions_notes_3'] = False
    
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
        context['is_current'] = True
    else:
        context['is_current'] = False
    
    if is_preview:
        try:
            context['article'] = VoyagesArticle.objects.get(issues__id=issue.id, is_reserved=False)
        except MultipleObjectsReturned:
            context['article'] = VoyagesArticle.objects.filter(issues__id=issue.id, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['article'] = False
    else:
        try:
            context['article'] = VoyagesArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
        except MultipleObjectsReturned:
            context['article'] = VoyagesArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['article'] = False
        
    if is_preview:
        try:
            context['archives'] = VoyagesArticle.objects.filter(is_reserved=False).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives'] = False
    else:
        try:
            context['archives'] = VoyagesArticle.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives'] = False
        
    return render_to_response('front/voyages.html', context, context_instance=RequestContext(request))



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
        context['is_current'] = True
    else:
        context['is_current'] = False
    
    # Types
    type_cotefumeurs = EpicurienArticleType.objects.get(slug='cote-fumeurs')
    type_cotegourmets = EpicurienArticleType.objects.get(slug='cote-gourmets')
    type_cotebar = EpicurienArticleType.objects.get(slug='cote-bar')
    
    # Côté fumeurs
    if is_preview:
        try:
            context['article_cotefumeurs'] = EpicurienArticle.objects.get(issues__id=issue.id, is_reserved=False, type=type_cotefumeurs)
        except MultipleObjectsReturned:
            context['article_cotefumeurs'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_reserved=False, type=type_cotefumeurs)[0]
        except ObjectDoesNotExist:
            context['article_cotefumeurs'] = False
    else:
        try:
            context['article_cotefumeurs'] = EpicurienArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type_cotefumeurs)
        except MultipleObjectsReturned:
            context['article_cotefumeurs'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type_cotefumeurs)[0]
        except ObjectDoesNotExist:
            context['article_cotefumeurs'] = False
    
    if is_preview:
        try:
            context['archives_cotefumeurs'] = EpicurienArticle.objects.filter(is_reserved=False, type=type_cotefumeurs).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotefumeurs'] = False
    else:
        try:
            context['archives_cotefumeurs'] = EpicurienArticle.objects.filter(is_ready_to_publish=True, is_reserved=False, type=type_cotefumeurs).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotefumeurs'] = False
    
    # Côté Gourmets
    if is_preview:
        try:
            context['article_cotegourmets'] = EpicurienArticle.objects.get(issues__id=issue.id, is_reserved=False, type=type_cotegourmets)
        except MultipleObjectsReturned:
            context['article_cotegourmets'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_reserved=False, type=type_cotegourmets)[0]
        except ObjectDoesNotExist:
            context['article_cotegourmets'] = False
    else:
        try:
            context['article_cotegourmets'] = EpicurienArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type_cotegourmets)
        except MultipleObjectsReturned:
            context['article_cotegourmets'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type_cotegourmets)[0]
        except ObjectDoesNotExist:
            context['article_cotegourmets'] = False
    
    if is_preview:
        try:
            context['archives_cotegourmets'] = EpicurienArticle.objects.filter(is_reserved=False, type=type_cotegourmets).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotegourmets'] = False
    else:
        try:
            context['archives_cotegourmets'] = EpicurienArticle.objects.filter(is_ready_to_publish=True, is_reserved=False, type=type_cotegourmets).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotegourmets'] = False
    
    # Côté Bar
    if is_preview:
        try:
            context['article_cotebar'] = EpicurienArticle.objects.get(issues__id=issue.id, is_reserved=False, type=type_cotebar)
        except MultipleObjectsReturned:
            context['article_cotebar'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_reserved=False, type=type_cotebar)[0]
        except ObjectDoesNotExist:
            context['article_cotebar'] = False
    else:
        try:
            context['article_cotebar'] = EpicurienArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type_cotebar)
        except MultipleObjectsReturned:
            context['article_cotebar'] = EpicurienArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False, type=type_cotebar)[0]
        except ObjectDoesNotExist:
            context['article_cotebar'] = False
    
    if is_preview:
        try:
            context['archives_cotebar'] = EpicurienArticle.objects.filter(is_reserved=False, type=type_cotebar).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotebar'] = False
    else:
        try:
            context['archives_cotebar'] = EpicurienArticle.objects.filter(is_ready_to_publish=True, is_reserved=False, type=type_cotebar).order_by('-publication_date')[:10]
        except ObjectDoesNotExist:
            context['archives_cotebar'] = False

    return render_to_response('front/epicurien.html', context, context_instance=RequestContext(request))



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
        context['is_current'] = True
    else:
        context['is_current'] = False
    
    if is_preview:
        try:
            context['article'] = AngerArticle.objects.get(issues__id=issue.id, is_reserved=False)
        except MultipleObjectsReturned:
            context['article'] = AngerArticle.objects.filter(issues__id=issue.id, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['article'] = False
    else:
        try:
            context['article'] = AngerArticle.objects.get(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)
        except MultipleObjectsReturned:
            context['article'] = AngerArticle.objects.filter(issues__id=issue.id, is_ready_to_publish=True, is_reserved=False)[0]
        except ObjectDoesNotExist:
            context['article'] = False
    
    if is_preview:
        try:
            context['archives'] = AngerArticle.objects.filter(is_reserved=False)
        except ObjectDoesNotExist:
            context['archives'] = False
    else:
        try:
            context['archives'] = AngerArticle.objects.filter(is_ready_to_publish=True, is_reserved=False)
        except ObjectDoesNotExist:
            context['archives'] = False
        
    return render_to_response('front/anger.html', context, context_instance=RequestContext(request))



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
    return render_to_response('front/tags.html', context, context_instance=RequestContext(request))


    
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
    
    articles = TaggedItem.objects.get_by_model(Article.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date'), tag)
    if articles:
        for article in articles:
            items.append((article.id, article))
    
    notes = TaggedItem.objects.get_by_model(Note.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date'), tag)
    if notes:
        for note in notes:
            items.append((note.id, note))
        
    regions = TaggedItem.objects.get_by_model(RegionNote.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date'), tag)
    if regions:
        for region in regions:
            items.append((region.id, region))
            
    voyages = TaggedItem.objects.get_by_model(VoyagesArticle.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date'), tag)
    if voyages:
        for voyage in voyages:
            items.append((voyage.id, voyage))
            
    epicurien = TaggedItem.objects.get_by_model(EpicurienArticle.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date'), tag)
    if epicurien:
        for e in epicurien:
            items.append((e.id, e))
            
    anger = TaggedItem.objects.get_by_model(AngerArticle.objects.filter(is_ready_to_publish=True, is_reserved=False).order_by('-publication_date'), tag)
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

    return render_to_response('front/tags_tag.html', context, context_instance=RequestContext(request))



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
    return render_to_response('front/rss_index.html', context, context_instance=RequestContext(request))



# Pages
# ------------------------------------------------------------------------------
def page(request, page_slug):
    """
    Displays a given page by its slug.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    context['page'] = get_object_or_404(Page.objects.all(), slug=page_slug, is_published=True)
    return render_to_response('front/page.html', context, context_instance=RequestContext(request))



