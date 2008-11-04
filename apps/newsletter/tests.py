# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.newsletter`` application.

"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


class SubscriberTest(TestCase):
    """
    Newsletter subscriber test.
    
    """
    fixtures = ['sample_data']

    def _test_subscriber(self, fields):
        """
        Private: returns the result of a POST query using the subscriber form.
        
        """
        return self.client.post(reverse('newsletter'), fields)
        
    def test_subscriber_form_get(self):
        """
        GET request on subscriber form.
        
        """
        response = self.client.get(reverse('newsletter'))
        self.assertEquals(response.status_code, 200)

    def test_subscriber_form_ok(self):
        """
        Subscriber form processing.
        
        """
        fields = {
            'first_name': 'Gilles',
            'last_name': 'Fabio',
            'email': 'gfabio@interfaceip.fr',
            'zip_code': '06700',
        }
        response = self._test_subscriber(fields)
        self.assertRedirects(response, reverse('newsletter_thanks'), status_code=302, target_status_code=200)

    def test_subscriber_form_empty(self):
        """
        Empty subscriber form.
        
        """
        fields = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'zip_code': '',
        }
        response = self._test_subscriber(fields)
        self.assertFormError(response, 'form', 'first_name', _('This field is required.'))
        self.assertFormError(response, 'form', 'last_name', _('This field is required.'))
        self.assertFormError(response, 'form', 'email', _('This field is required.'))
        self.assertFormError(response, 'form', 'zip_code', _('This field is required.'))

    def test_subscriber_wrong_email(self):
        """
        Subscriber form with a wrong email.
        
        """
        fields = {
            'first_name': 'Gilles',
            'last_name': 'Fabio',
            'email': 'azerty',
            'zip_code': '06000',
        }
        response = self._test_subscriber(fields)
        self.assertFormError(response, 'form', 'email', _('Enter a valid e-mail address.'))

    def test_subscriber_already_registered_email(self):
        """
        Subscriber form with an email already registered.
        
        """
        email1_fields = {
            'first_name': 'Gilles',
            'last_name': 'Fabio',
            'email': 'gfabio@interfaceip.fr',
            'zip_code': '06000',
        }
        
        email2_fields = {
            'first_name': 'Gilles',
            'last_name': 'Fabio',
            'email': 'gfabio@interfaceip.fr',
            'zip_code': '06000',
        }
        response = self._test_subscriber(email1_fields)
        response = self._test_subscriber(email2_fields)
        self.assertFormError(response, 'form', 'email', _('Subscriber with this Email already exists.'))

    def test_subscriber_wrong_zip_code(self):
        """
        Subscriber form with a wrong zip code.
        
        """
        fields = {
            'first_name': 'Gilles',
            'last_name': 'Fabio',
            'email': 'gfabio@interfaceip.fr',
            'zip_code': '060',
        }
        response = self._test_subscriber(fields)
        self.assertFormError(response, 'form', 'zip_code', _('Enter a zip code in the format XXXXX.'))



