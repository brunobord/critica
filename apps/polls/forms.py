# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.polls`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.polls.models import Poll


class PollAdminModelForm(forms.ModelForm):
    """
    Poll admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='polls.poll'), required=False)
    
    class Meta:
        model = Poll


