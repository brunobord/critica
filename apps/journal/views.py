"""
Views for ``critica.apps.journal``.

"""
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import Http404
from critica.apps.journal.models import Page, Issue, Article


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


def archives(request):
    """
    Displays archives index page.
    
    """
    issues = Issue.complete.all()
    
    return render_to_response(
        'journal/archives.html', 
        {'issues': issues}, 
        context_instance=RequestContext(request)
    )
    
    
def archives_issue(request, issue):
    """
    Displays archives for a given issue.
    
    """
    issue = get_object_or_404(Issue.complete.all(), number=issue)
    return render_to_response(
        'journal/archives_issue.html', 
        {'issue': issue}, 
        context_instance=RequestContext(request)
    )


def archives_issue_category(request, issue, category):
    """
    Displays archives for a given issue and a given category.
    
    """
    articles = get_list_or_404(Article.complete.all(), issues__number=issue, category__slug=category)
    return render_to_response(
        'journal/archives_issue_category.html', 
        {'articles': articles}, 
        context_instance=RequestContext(request)
    )


