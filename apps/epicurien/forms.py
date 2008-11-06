# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.epicurien`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.epicurien.models import EpicurienArticle


class EpicurienArticleAdminModelForm(forms.ModelForm):
    """
    Epicurien article admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='epicurien.epicurienarticle'), required=False)
    
    class Meta:
        model = EpicurienArticle
        

