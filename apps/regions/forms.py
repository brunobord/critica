# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.regions`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.regions.models import RegionNote


class RegionNoteAdminModelForm(forms.ModelForm):
    """
    Region note admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='regions.regionnote'), required=False)
    
    class Meta:
        model = RegionNote


