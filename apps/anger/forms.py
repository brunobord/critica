# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.anger`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.anger.models import AngerArticle


class AngerArticleAdminModelForm(forms.ModelForm):
    """
    Anger article admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='anger.angerarticle'), required=False)
    
    class Meta:
        model = AngerArticle


