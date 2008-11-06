# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.voyages`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.voyages.models import VoyagesArticle


class VoyagesArticleAdminModelForm(forms.ModelForm):
    """
    Voyages article admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='voyages.voyagesarticle'), required=False)
    
    class Meta:
        model = VoyagesArticle


