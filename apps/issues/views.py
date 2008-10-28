# -*- coding: utf-8 -*-
"""
Views of ``critica.apps.issues`` application.

"""
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from critica.apps.utils import urlbase64
from critica.apps.issues.models import Issue


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
