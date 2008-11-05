#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage

from critica.apps.sendfriend.forms import SendFriendForm
from critica.apps.issues.views import _get_current_issue
from critica.apps.articles.models import Article
from critica.apps.regions.models import FeaturedRegion
from critica.apps.regions.models import RegionNote
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.anger.models import AngerArticle


def index(request):
    """
    View handling form requests.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    if request.method == 'POST':
        form = SendFriendForm(request.POST)
        if form.is_valid():
            sendfriend_send_mail(form)
            return HttpResponseRedirect(reverse('sendfriend_thanks'))
    else:
        form = SendFriendForm(auto_id=True)
        
    context['form'] = form

    return direct_to_template(request, 'sendfriend/form_page.html', context)


def sendfriend_send_mail(form):
    """
    Generates and sends email.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    all_items = []
    # Articles standard categories
    articles = Article.published.filter(issues__id=issue.id)
    for a in articles:
        all_items.append((a.id, a))
    # Regions
    featured = FeaturedRegion.objects.get(issue=issue)
    region_note = RegionNote.published.filter(region=featured.region, issues__id=issue.id)[0]
    all_items.append((region_note.id, region_note))
    # Voyages
    articles_voyages = VoyagesArticle.published.filter(issues__id=issue.id)
    for a in articles_voyages:
        all_items.append((a.id, a))
    # Epicurien
    articles_epicurien = EpicurienArticle.published.filter(issues__id=issue.id)
    for a in articles_epicurien:
        all_items.append((a.id, a))
    # Anger
    articles_anger = AngerArticle.published.filter(issues__id=issue.id)
    for a in articles_anger:
        all_items.append((a.id, a))
    items = [item for k, item in all_items]
    
    context['items'] = items
    context['sender'] = form.cleaned_data['sender']
    context['message'] = form.cleaned_data['message']
    
    body = render_to_string('sendfriend/email.html', context)
    subject = u'Critic@...'
    msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data['to_email']])
    msg.content_subtype = "html"
    msg.send()


def thanks(request):
    """
    View of thanks message.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    return direct_to_template(request, 'sendfriend/thanks.html', context)


