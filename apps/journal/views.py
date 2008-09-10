"""
Views for ``critica.apps.journal``.

"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from critica.apps.journal.models import Page


def home(request):
    """
    Displays the homepage.
            
    """
    page = Page.complete.get(category__pk=1)
    articles = page.articles.all()
    
    return render_to_response(
        'journal/home.html', 
        {'page': page, 'articles': articles},
        context_instance=RequestContext(request)
    )


def category(request, category):
    """
    Displays the category page for a given category.
    
    """
    try:
        page = Page.complete.get(category__slug=category)
        articles = page.articles.all()
    except:
        raise Http404
        
    return render_to_response(
        'journal/category.html', 
        {'page': page, 'articles': articles}, 
        context_instance=RequestContext(request)
    )

