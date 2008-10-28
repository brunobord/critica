# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.sendfriend`` application.

"""
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext as _


class ShareTestCase(TestCase):
    """
    Send friend test case.
    
    """
    def _test_share(self, fields):
        """
        Private: returns the result of a POST query using the share form.
        """
        return self.client.post(reverse('share'), fields)


    def test_share_form_get(self):
        """
        What do we do with a 'get' request.
        
        """
        response = self.client.get(reverse('share'))
        self.assertEquals(response.status_code, 200)


    def test_share_form_ok(self):
        """
        Share form processing.
        
        """
        fields = {
            'to_email': 'gfabio@interfaceip.com',
        }
        response = self._test_share(fields)
        self.assertRedirects(response, reverse('share_ok'), status_code=302, target_status_code=200)
        self.assertEquals(len(mail.outbox), 1) # 1 mail sent
        self.assertEquals(mail.outbox[0].to, [fields['to_email']])
        self.assertEquals(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        # testing body
        self.assertTrue(mail.outbox[0].body.startswith('Bonjour,'))
        html_attachment = mail.outbox[0].attachments[0] # it's a tuple
        self.assertTrue(html_attachment[1].startswith('<p>Bonjour,'))


    def test_share_form_empty(self):
        """
        Empty form, error.
        
        """
        response = self._test_share({'to_email': ''})
        self.assertFormError(response, "form", 'to_email', _('This field is required.'))


    def test_share_wrong_email(self):
        """
        Empty form, error.
        
        """
        response = self._test_share({'to_email': 'ddd'})
        self.assertFormError(response, "form", 'to_email', _('Enter a valid e-mail address.'))



