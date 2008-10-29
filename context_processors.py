"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

"""
from critica.apps.issues.models import Issue


def current_issue(request):
    """ 
    Returns the current issue object and the last 20 issues. 
    
    """
    context = {}
    try:
        current_issue = Issue.published.all()[0]
        context['current_issue'] = current_issue
    except IndexError:
        context['current_issue'] = None
    
    try:
        issuepreviews = Issue.objects.all()[:20]
        context['issuepreviews'] = issuepreviews
    except IndexError:
        context['issuepreviews'] = None
        
    return context

