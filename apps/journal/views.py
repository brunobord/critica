"""
Views for ``critica.apps.journal``.

"""
from django.shortcuts import render_to_response
from critica.apps.journal.models import Page


def home(request):
    page = Page.complete.filter(is_cover=True)[0]
    return render_to_response('journal/home.html', {'page': page})
    
def category(request, category):
    page = Page.complete.filter(category__slug=category)[0]
    return render_to_response('journal/category.html', {'page': page})
    
def archives(request):
    return render_to_response('journal/archives.html', {})
    
def archives_issue(request, issue):
    return render_to_response('journal/archives_issue.html', {})
    
def archives_issue_category(request, issue, category):
    return render_to_response('journal/archives_issue_category.html', {})
    
def archives_issue_article(request, issue, category, article):
    return render_to_response('journal/archives_issue_article.html', {})
    

