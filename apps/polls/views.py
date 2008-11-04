# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.polls`` application.

"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from critica.apps.issues.views import _get_current_issue
from critica.apps.polls.models import Poll
from critica.apps.polls.models import Choice
from critica.apps.polls.models import Vote


def poll_vote(request):
    """
    View of poll vote.
    
    """
    if request.method == 'POST':
        if request.POST.has_key('id_choice'):
            if request.POST['id_choice']:
                id_poll = request.POST['id_poll']
                id_choice = request.POST['id_choice']
                ip_address = request.POST['ip_address']
                poll = Poll.objects.get(pk=id_poll)
                choice = Choice.objects.get(pk=id_choice)
                vote = Vote(poll=poll, choice=choice, ip_address=ip_address)
                vote.save()
                return HttpResponseRedirect(reverse('poll_results', args=[poll.slug]))
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))


def poll_results(request, poll_slug):
    """
    View of polls results.
    
    """
    context = {}
    issue = _get_current_issue()
    context['issue'] = issue
    context['is_current'] = True
    
    poll = get_object_or_404(Poll.published.all(), slug=poll_slug)
    context['poll'] = poll
    
    return direct_to_template(request, 'polls/results.html', context)


