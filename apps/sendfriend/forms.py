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
    sender   = forms.CharField(label='Votre nom', required=True)
    to_email = forms.EmailField(label='Email de votre ami', required=True)
