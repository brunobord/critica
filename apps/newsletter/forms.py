# -*- coding: utf-8 -*-
"""
Forms of ``critica.apps.newsletter`` application.


"""
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.localflavor.fr.forms import FRZipCodeField
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from critica.apps.newsletter.models import Subscriber


class SubscriberForm(forms.ModelForm):
    """
    Newsletter subscriber form.
    
    """
    first_name = forms.CharField(label='prénom', required=True)
    last_name = forms.CharField(label='nom', required=True)
    email = forms.EmailField(label='email', required=True)
    zip_code = FRZipCodeField(label=_('zip code'))
    
    class Meta:
        model = Subscriber


class UnsubscribeForm(forms.Form):
    """
    Newsletter Unsubscribe form.
    
    """
    email = forms.EmailField(label=_('your email'), required=True)
    
    def clean(self):
        """
        Validation process.
        
        """
        if self.cleaned_data.has_key('email'):
            try:
                subscriber = Subscriber.objects.get(email=self.cleaned_data['email'])
            except ObjectDoesNotExist:
                msg = _('Sorry, unknown email. This email has not been registered.')
                self._errors['email'] = ErrorList([msg])
        return self.cleaned_data

