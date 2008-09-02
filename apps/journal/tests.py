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
        
    def test_archives(self):
        """
        Tests archives.
        Should return 200 and use ``journal/archives.html`` template.
        """
        response = self.client.get('/archives/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives.html')

    def test_archives_issue(self):
        """
        Tests issue.
        Should return 200 and use ``journal/archives_issue.html`` template.
        """
        response = self.client.get('/archives/114/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives_issue.html')
        
    def test_archives_issue_not_found(self):
        """
        Tests an unexistent issue.
        Should return 404.
        """
        response = self.client.get('/archives/850/')
        self.assertEqual(response.status_code, 404)
        
    def test_archives_issue_category(self):
        """
        Tests an archived issue category.
        Should return 200 and use ``journal/archives_issue_category.html`` template.
        """
        response = self.client.get('/archives/114/sports/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives_issue_category.html')
        
    def test_archives_issue_category_not_found(self):
        """
        Tests an unexistent archived issue category.
        Should return 404.
        """
        response = self.client.get('/archives/114/doesnotexist/')
        self.assertEqual(response.status_code, 404)
        
    def test_archives_issue_article(self):
        """
        Tests archived issue article.
        Should return 200 and use ``journal/archives_issue_article.html`` template.
        """
        response = self.client.get('/archives/114/sport/aviron-bayonnais/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/archives_issue_article.html')
        
    def test_archives_issue_article_not_found(self):
        """
        Tests an unexistent archived issue article.
        Should return 404.
        """
        response = self.client.get('/archives/114/sport/does-not-exist/')
        self.assertEqual(response.status_code, 404)

