# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.newsletter`` application.

"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from critica.apps.newsletter.models import Subscriber
from critica.apps.newsletter.forms import SubscriberForm
from critica.apps.newsletter.forms import UnsubscribeForm
from critica.apps.issues.views import _get_current_issue


def subscribe_form(request):
    """
    View of newsletter subscribing form.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('newsletter_subscribe_thanks'))
    else:
        form = SubscriberForm(auto_id=True)
        
    context['form'] = form
    return direct_to_template(request, 'newsletter/subscribe_form.html', context)


def subscribe_thanks(request):
    """
    View of newsletter subscribing thanks message.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    return direct_to_template(request, 'newsletter/subscribe_thanks.html', context)
    

def unsubscribe_form(request):
    """
    View of newsletter unsubscribing form.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            subscriber = Subscriber.objects.get(email=form.cleaned_data['email'])
            subscriber.delete()
            return HttpResponseRedirect(reverse('newsletter_unsubscribe_thanks'))
    else:
        form = UnsubscribeForm(auto_id=True)
    context['form'] = form
    return direct_to_template(request, 'newsletter/unsubscribe_form.html', context)
    
    
def unsubscribe_thanks(request):
    """
    View of newsletter unsubscribe thanks message.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    return direct_to_template(request, 'newsletter/unsubscribe_thanks.html', context)


@login_required
def admin_preview(request, format, issue_number):
    """
    View of newsletter admin preview.
    
    Two required parameters::
    
        format
            Should be: 'text' or 'html' (available in 'authorized_formats').
            
        issue_number
            Should be the number of issue.
    
    """
    authorized_formats = ['txt', 'html']
    
    context = {}
    
    # Issue number
    issue_number = int(issue_number)
    
    # Check format
    if format in authorized_formats:
        format = format
    else:
        format = 'html'
    
    # Set template
    if format == 'html':
        template = 'newsletter/preview.html'
        mimetype = 'text/html'
    if format == 'txt':
        template = 'newsletter/preview.txt'
        mimetype = 'text/plain'
    
    # Populate context
    from critica.apps.issues.models import Issue
    from critica.apps.articles.models import Article
    from critica.apps.epicurien.models import EpicurienArticle
    from critica.apps.voyages.models import VoyagesArticle
    from critica.apps.anger.models import AngerArticle
    from critica.apps.regions.models import FeaturedRegion
    from critica.apps.regions.models import RegionNote
    from critica.apps.illustrations.models import IllustrationOfTheDay
    from critica.apps.polls.models import Poll
    
    context['newsletter_issue'] = Issue.objects.get(number=issue_number)
    
    articles = Article.objects.filter(issues__number=issue_number)
    for article in articles:
        varname = u'article_%s' % article.category.slug
        context[varname] = article
        
    context['epicurien_article_cotegourmets'] = EpicurienArticle.objects.filter(issues__number=issue_number, type__id=1).order_by('-publication_date')[0:1].get()
    context['epicurien_article_cotebar'] = EpicurienArticle.objects.filter(issues__number=issue_number, type__id=2).order_by('-publication_date')[0:1].get()
    context['epicurien_article_cotefumeurs'] = EpicurienArticle.objects.filter(issues__number=issue_number, type__id=3).order_by('-publication_date')[0:1].get()
    context['voyages_article'] = VoyagesArticle.objects.filter(issues__number=issue_number).order_by('-publication_date')[0:1].get()
    context['anger_article'] = AngerArticle.objects.filter(issues__number=issue_number).order_by('-publication_date')[0:1].get()
    context['illustration'] = IllustrationOfTheDay.objects.filter(issues__number=issue_number).order_by('-creation_date')[0:1].get()
    context['poll'] = Poll.objects.filter(issues__number=issue_number).order_by('-creation_date')[0:1].get()
    featured_region = FeaturedRegion.objects.get(issue__number=issue_number)
    context['featured_region_note'] = RegionNote.objects.get(issues__number=issue_number, region=featured_region)

    return direct_to_template(request, template=template, mimetype=mimetype, extra_context=context)
    
    
    
    
    
