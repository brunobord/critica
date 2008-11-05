# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.sendfriend`` application.

"""
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext as _


class SendFriendTestCase(TestCase):
    """
    SendFriend application test case.
    
    """
    fixtures = ['sample_data']

    def _test_sendfriend(self, fields):
        """
        Private: returns the result of a POST query using the sendfriend form."
        
        """
        return self.client.post(reverse('sendfriend_index'), fields)

    def test_sendfriend_form_get(self):
        """
        GET request on sendfriend form.
        
        """
        response = self.client.get(reverse('sendfriend_index'))
        self.assertEquals(response.status_code, 200)

    def test_sendfriend_form_ok(self):
        """
        SendFriend form processing.
        
        """
        fields = {
            'sender': 'Gilles Fabio',
            'to_email': 'gfabio@interfaceip.com',
        }
        response = self._test_sendfriend(fields)
        self.assertRedirects(response, reverse('sendfriend_thanks'), status_code=302, target_status_code=200)
        self.assertEquals(len(mail.outbox), 1) # 1 mail sent
        self.assertEquals(mail.outbox[0].to, [fields['to_email']])
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertTrue(mail.outbox[0].body.startswith('<p>Bonjour,'))

    def test_sendfriend_form_empty(self):
        """
        Empty sendfriend form.
        
        """
        fields = {
            'sender': '',
            'to_email': '',
        }
        response = self._test_sendfriend(fields)
        self.assertFormError(response, 'form', 'sender', _('This field is required.'))
        self.assertFormError(response, 'form', 'to_email', _('This field is required.'))

    def test_sendfriend_wrong_email(self):
        """
        SendFriend form with a wrong email.
        
        """
        fields = {
            'sender': 'Gilles Fabio',
            'to_email': 'azerty',
        }
        response = self._test_sendfriend(fields)
        self.assertFormError(response, 'form', 'to_email', _('Enter a valid e-mail address.'))



