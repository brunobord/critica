# -*- coding: utf-8 -*-
"""
Forms for ``critica.apps.sendfriend`` application.

"""
from django import forms
from django.utils.translation import ugettext_lazy as _


class SendFriendForm(forms.Form):
    """
    Form to send latest articles to a friend.
    
    """
    to_email = forms.EmailField(label=_('to email'))
