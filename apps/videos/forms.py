# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.videos`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.videos.models import Video


class VideoAdminModelForm(forms.ModelForm):
    """
    Video admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='videos.video'), required=False)
    
    class Meta:
        model = Video

