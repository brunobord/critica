# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.sendfriend`` application.

"""
from django.conf import settings
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext as _


class SendFriendTestCase(TestCase):
    """
    Send friend test case.
    
    """
    def _test_sendfriend(self, fields):
        """
        Private: returns the result of a POST query using the send friend form.
        
        """
        return self.client.post(reverse('sendfriend'), fields)


    def test_sendfriend_form_get(self):
        """
        What do we do with a 'get' request.
        
        """
        response = self.client.get(reverse('sendfriend'))
        self.assertEquals(response.status_code, 200)


    def test_sendfriend_form_ok(self):
        """
        Send friend form processing.
        
        """
        fields = {
            'to_email': 'gfabio@interfaceip.com',
        }
        response = self._test_sendfriend(fields)
        self.assertRedirects(response, reverse('sendfriend_ok'), status_code=302, target_status_code=200)
        self.assertEquals(len(mail.outbox), 1) # 1 mail sent
        self.assertEquals(mail.outbox[0].to, [fields['to_email']])
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        # testing body
        self.assertTrue(mail.outbox[0].body.startswith('<p>Bonjour,'))


    def test_sendfriend_form_empty(self):
        """
        Empty form, error.
        
        """
        response = self._test_sendfriend({'to_email': ''})
        self.assertFormError(response, "form", 'to_email', _('This field is required.'))


    def test_sendfriend_wrong_email(self):
        """
        Empty form, error.
        
        """
        response = self._test_sendfriend({'to_email': 'ddd'})
        self.assertFormError(response, "form", 'to_email', _('Enter a valid e-mail address.'))



