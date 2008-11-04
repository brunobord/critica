# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.newsletter`` application.


"""
from django import forms
from django.contrib.localflavor.fr.forms import FRZipCodeField
from django.utils.translation import ugettext_lazy as _
from critica.apps.newsletter.models import Subscriber


class SubscriberForm(forms.ModelForm):
    """
    Newsletter subscriber form.
    
    """
    zip_code = FRZipCodeField(label=_('zip code'))
    
    class Meta:
        model = Subscriber


