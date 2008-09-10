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
        Should return 200 and use ``journal/issue_archive.html`` template.
        
        """
        response = self.client.get('/archives/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/issue_archive.html')
        
    def test_archives_year(self):
        """
        Tests archives for a given year.
        Should return 200 and use ``journal/issue_archive_year.html`` template.
        
        """
        response = self.client.get('/archives/2008/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/issue_archive_year.html')
        
    def test_archives_year_not_found(self):
        """
        Tests archives for an unexistent year.
        Should return 404.
        
        """
        response = self.client.get('/archives/2002/')
        self.assertEqual(response.status_code, 404)
        
    def test_archives_month(self):
        """
        Tests archives for a given month.
        Should return 200 and use ``journal/issue_archive_month.html`` template.
        
        """
        response = self.client.get('/archives/2008/09/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/issue_archive_month.html')
        
    def test_archives_month_not_found(self):
        """
        Tests archives for an unexistent month.
        Should return 404.
        
        """
        response = self.client.get('/archives/2008/02/')
        self.assertEqual(response.status_code, 404)
        
    def test_archives_day(self):
        """
        Tests archives for a given day.
        Should return 200 and use ``journal/issue_archive_day.html`` template.
        
        """
        response = self.client.get('/archives/2008/09/08/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/issue_archive_day.html')
        
    def test_archives_day_not_found(self):
        """
        Tests archives for an unexistent day.
        Should return 404.
        
        """
        response = self.client.get('/archives/2008/09/07/')
        self.assertEqual(response.status_code, 404)


