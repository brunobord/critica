# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.notes`` application.

"""
from django import forms
from tagging.forms import TagField
from critica.lib.widgets import AutoCompleteTagInput
from critica.apps.notes.models import Note


class NoteAdminModelForm(forms.ModelForm):
    """
    Note admin custom form.
    
    """
    tags = TagField(widget=AutoCompleteTagInput(model='notes.note'), required=False)
    
    class Meta:
        model = Note


