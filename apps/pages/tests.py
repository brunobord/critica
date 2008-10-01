# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.pages`` application.

"""
from django.test import TestCase


class PagesTestCase(TestCase):
    """
    Pages test case.
    
    """
    fixtures = ['sample_data']
    
    def test_published_page(self):
        """
        Tests a published page.
        Should return 200 and use ``pages/page_detail.html`` template.
        
        """
        response = self.client.get('/pages/mentions-legales/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/page_detail.html')
        
    def test_unpublished_page(self):
        """
        Tests an unexistent page.
        Should return 404.
        
        """
        response = self.client.get('/pages/unpublished-page/')
        self.assertEqual(response.status_code, 404)

