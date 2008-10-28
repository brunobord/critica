#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.core import mail
from django.core.mail import EmailMultiAlternatives

from critica.apps.sendfriend.forms import SendFriendForm
from critica.apps.front.views import _get_current_issue


def sendfriend(request):
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
        form = SendFriendForm()
        
    context['form'] = form

    return direct_to_template(request, 'sendfriend/form_page.html', context)


def sendfriend_send_mail(form):
    """
    Generates and sends email.
    
    """
    body_txt = render_to_string('sendfriend/email_text.html')
    body_html = render_to_string('sendfriend/email_html.html')
    subject = u'Critic@...'
    msg = EmailMultiAlternatives(subject, body_txt, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data['to_email']])
    msg.attach_alternative(body_html, "text/html")
    msg.send()


def sendfriend_thanks(request):
    """
    View of thanks message.
    
    """
    issue = _get_current_issue()
    context = {}
    context['issue'] = issue
    context['is_current'] = True
    
    return direct_to_template(request, 'sendfriend/thanks.html', context)


