# -*- coding utf-8 -*-
"""
Positions application custom forms.

"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms.util import ErrorList
from critica.apps.positions.models import CategoryPosition
from critica.apps.positions.models import NotePosition
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.positions.models import IssueNotePosition


class CustomIssueCategoryPositionForm(forms.ModelForm):
    """
    Custom form of IssueCategoryPosition model.
    
    """
    class Meta:
        model = IssueCategoryPosition
        
    def clean(self):
        issue = self.cleaned_data['issue']
        category = self.cleaned_data['category']
        position = self.cleaned_data['position']
        
        issue_positions = IssueCategoryPosition.objects.filter(issue=issue).exclude(category=category)
        all_positions = CategoryPosition.objects.all()
        all_issue_positions = [item.position for item in issue_positions]
        diff_list = [item for item in all_positions if not item in all_issue_positions]
        availables = [item.name for item in diff_list]
        
        for issue_position in issue_positions:
            if position == issue_position.position and position != None:
                msg = _('Sorry, this position is already taken. Available position(s): %(availables)s') % {'availables': ', '.join(availables)}
                self._errors['position'] = ErrorList([msg])
        
        return self.cleaned_data
        
        
class CustomIssueNotePositionForm(forms.ModelForm):
    """
    Custom form of IssueNotePosition model.
    
    """
    class Meta:
        model = IssueNotePosition
        
    def clean(self):
        issue = self.cleaned_data['issue']
        category = self.cleaned_data['category']
        type = self.cleaned_data['type']
        position = self.cleaned_data['position']
        
        note_positions = IssueNotePosition.objects.filter(issue=issue, category=category).exclude(type=type)
        all_positions = NotePosition.objects.all()
        all_note_positions = [item.position for item in note_positions]
        diff_list = [item for item in all_positions if not item in all_note_positions]
        availables = [item.name for item in diff_list]
        
        for note_position in note_positions:
            if position == note_position.position and position != None:
                msg = _('Sorry, this position is already taken. Available position(s): %(availables)s') % {'availables': ', '.join(availables)}
                self._errors['position'] = ErrorList([msg])
        return self.cleaned_data

