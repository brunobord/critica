# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.tags`` application.

"""
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage
from tagging.models import Tag
from tagging.models import TaggedItem
from tagging.utils import calculate_cloud
from critica.apps.front.views import _get_current_issue
from critica.apps.articles.models import Article
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.anger.models import AngerArticle


def tags(request):
    """
    Displays all tags as tag cloud.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
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
        
    epicurien_tags = Tag.objects.usage_for_queryset(EpicurienArticle.published.all(), counts=True)
    for tag in epicurien_tags:
        all_tags.append(tag)
        
    anger_tags = Tag.objects.usage_for_queryset(AngerArticle.published.all(), counts=True)
    for tag in anger_tags:
        all_tags.append(tag)
        
    context['tags'] = calculate_cloud(all_tags, steps=10)
    
    return render_to_response(
        'tags/tags.html', 
        context, 
        context_instance=RequestContext(request))

    
def tag(request, tag):
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
        'tags/tag.html', 
        context, 
        context_instance=RequestContext(request))


