# -*- coding: utf-8 -*-
"""
Templatetags of ``critica.apps.utils`` application.

"""
from django import template
from BeautifulSoup import BeautifulStoneSoup
register = template.Library()


@register.filter
def replace_html_entities(value):
    """
    Takes a safe and strip-tagged string and replaces HTML entities by the
    corresponding Unicode characters.
    
    Example::
    
        article.content|safe|striptags|replace_html_entities
    
    """
    clean_content = BeautifulStoneSoup(value, convertEntities="html", smartQuotesTo="html").contents[0]
    return clean_content
replace_html_entities.is_safe = True

