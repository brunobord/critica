# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.custom_admin`` application.

"""
from django.test import TestCase


class AdminPreviewTestCase(TestCase):
    """
    Admin article / note previews test case.
    
    """
    fixtures = ['sample_data']
    
    def test_preview_home_article(self):
        response = self.client.get('/admin/preview/home/article/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/home_article.html')
        
    def test_preview_home_note(self):
        response = self.client.get('/admin/preview/home/note/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/home_note.html')
        
    def test_preview_category_article(self):
        response = self.client.get('/admin/preview/category/national/article/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/category_article.html')
        
    def test_preview_category_note(self):
        response = self.client.get('/admin/preview/category/national/note/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/category_note.html')
        
    def test_preview_category_voyages_article(self):
        response = self.client.get('/admin/preview/category/voyages/article/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/category_voyages_article.html')
        
    def test_preview_category_epicurien_article(self):
        response = self.client.get('/admin/preview/category/epicurien/article/1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/category_epicurien_article.html')
        
    def test_preview_category_anger_article(self):
        response = self.client.get('/admin/preview/category/coup-de-geule/article/1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('custom_admin/preview/category_anger_article.html')


