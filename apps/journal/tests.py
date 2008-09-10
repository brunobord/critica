# -*- coding: utf-8 -*-
"""
Tests for ``critica.apps.journal``.

"""
from django.test import TestCase


class JournalTestCase(TestCase):
    fixtures = ['sample_data']
    
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
        response = self.client.get('/national/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/category.html')
        
    def test_category_not_found(self):
        """
        Tests an unexistent current issue category.
        Should return 404.
        
        """
        response = self.client.get('/doesnotexist/')
        self.assertEqual(response.status_code, 404)
        
    def test_archives(self):
        """
        Tests archives index.
        Should returns 200 and use ``journal/archives.html`` template.
        
        """
        response = self.client.get('/archives/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives.html')
        
    def test_archives_issue(self):
        """
        Tests archives for a given issue.
        Should returns 200 and use ``journal/archives_issue.html`` template.
        
        """
        response = self.client.get('/archives/124/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives_issue.html')
        
    def test_archives_issue_not_found(self):
        """
        Tests archives for an unexistent issue.
        Should returns 404.
        
        """
        response = self.client.get('/archives/100/')
        self.assertEqual(response.status_code, 404)

    def test_archives_issue_category(self):
        """
        Tests archives for a given issue and a given category.
        Should returns 200 and use ``journal/archives_issue_category.html`` template.
        
        """
        response = self.client.get('/archives/124/national/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives_issue_category.html')
        
    def test_archives_issue_category_not_found(self):
        """
        Tests archives for an unexistent issue category.
        Should returns 404.
        
        """
        response = self.client.get('/archives/124/doesnotexist/')
        self.assertEqual(response.status_code, 404)

    def test_archives_bad_issue_with_existent_category(self):
        """
        Tests archives for an unexistent issue with an existent issue category.
        Should returns 404.
        
        """
        response = self.client.get('/archives/100/national/')
        self.assertEqual(response.status_code, 404)
        

