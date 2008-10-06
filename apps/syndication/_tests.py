# -*- coding: utf-8 -*-
"""
Tests for ``critica.apps.syndication``.

"""
from django.test import TestCase
from critica.apps.categories.models import Category


class SyndicationTestCase(TestCase):
    fixtures = ['sample_data']
    
    def test_rss_index(self):
        """
        Tests RSS index page.
        Should return 200 and use ``syndication/index.html`` template.
        
        """
        response = self.client.get('/rss/')
        self.assertEqual(response.status_code, 200)


    def test_rss_articles(self):
        """
        Tests latest articles RSS feed.
        Should return 200.
        
        """
        response = self.client.get('/rss/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/rss+xml')


    def test_rss_category(self):
        """
        Tests category RSS feed.
        Should return 200.
        
        """
        categories = Category.objects.all()
        for category in categories:
            url = '/rss/rubriques/%s/' % category.slug
            if not category.id == 1:
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['Content-Type'], 'application/rss+xml')


    def test_rss_category_not_found(self):
        """
        Tests an unexistent category RSS feed.
        Should return 200.
        
        """
        response = self.client.get('/rss/rubriques/doesnotexist/')
        self.assertEqual(response.status_code, 404)


