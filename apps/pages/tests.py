# -*- coding: utf-8 -*-
"""
Tests for ``critica.apps.pages``.

"""
from django.test import TestCase
from critica.apps.pages.models import Page


class PagesTestCase(TestCase):
    fixtures = ['test_data']

    def test_slugify_page_title(self):
        pass
    
    def test_absolute_url(self):
        page = Page.objects.get(slug='test-page')
        self.assertEqual(page.get_absolute_url(), '/pages/test-page/')
    
    def test_published_page(self):
        response = self.client.get('/pages/test-page/')
        self.assertEqual(response.status_code, 200)
        
    def test_unpublished_page(self):
        response = self.client.get('/pages/unpublished-page/')
        self.assertEqual(response.status_code, 404)
        
    def test_page_template(self):
        response = self.client.get('/pages/test-page/')
        self.assertTemplateUsed(response, 'pages/page_detail.html')

