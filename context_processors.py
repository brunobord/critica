"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

"""
from critica.apps.issues.models import Issue


def current_issue(request):
    """ Returns the current complete issue object. """
    context_extras = {}
    current_issue = Issue.published.all()[0:1]
    context_extras['current_issue'] = current_issue
    return context_extras

