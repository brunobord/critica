# -*- coding: utf-8 -*-
"""
Tests for ``critica.apps.journal``.

"""
from django.test import TestCase


class JournalTestCase(TestCase):
    fixtures = ['test_data']
    
    def test_home(self):
        """
        Tests homepage.
        Should return 200 and use ``journal/home.html`` template.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/home.html')
        
    def test_category(self):
        """
        Tests a current issue category.
        Should return 200 and use ``journal/category.html`` template.
        """
        response = self.client.get('/test-category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/category.html')
        
    def test_category_not_found(self):
        """
        Tests an unexistent current issue category.
        Should return 404.
        """
        response = self.client.get('/doesnotexist/')
        self.assertEqual(response.status_code, 404)

