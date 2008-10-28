# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.search`` application.

"""
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage

from critica.apps.front.views import _get_current_issue
from critica.apps.articles.models import Article
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.anger.models import AngerArticle


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
        'search/search_results.html',
        context,
        context_instance=RequestContext(request)
    )

