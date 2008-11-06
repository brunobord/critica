# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.articles`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.articles.models import Article


class ArticleAdminModelForm(forms.ModelForm):
    """
    Article admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='articles.article'), required=False)
    
    class Meta:
        model = Article


