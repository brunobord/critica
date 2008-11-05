# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.issues_preview`` application.

"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from critica.apps.issues.models import Issue

# Issue to test
ISSUE_NUMBER = 136


class issues_previewTestCase(TestCase):
    """
    Issue preview test case.
    
    """
    fixtures = ['sample_data']
    

    def _get_issue_key(self):
        """
        Returns issue secret key.
        
        """
        issue = Issue.objects.get(number=ISSUE_NUMBER)
        return issue.secret_key
        
        
    def test_preview_home(self):
        """
        Tests issue preview for home.
        
        """
        # Get issue secret key
        sk = self._get_issue_key()
        # Should returns return 200
        response = self.client.get(reverse('issues_preview_home', args=[sk]))
        self.assertEqual(response.status_code, 200)
        # Checks if template is the good one and if we are in the current mode
        self.assertTemplateUsed(response, 'front/home.html')
        self.assertEqual(response.context[0]['is_current'], False)
        self.assertEqual(response.context[0]['is_preview'], True)
        self.assertEqual(response.context[0]['is_archive'], False)
        
    def test_preview_category(self):
        """
        Tests issue preview for category.
        
        """
        # Get issue secret key
        sk = self._get_issue_key()
        # Imports
        from critica.apps.categories.models import Category
        from critica.apps.notes.models import Note
        from critica.apps.articles.models import Article
        # Unstandard categories has to be removed
        EXCLUDED_CATEGORIES = ['coup-de-gueule', 'epicurien', 'voyages', 'regions']
        categories = Category.objects.exclude(slug__in=EXCLUDED_CATEGORIES)
        # Iterates categories
        for category in categories:
            # Should return 200
            response = self.client.get(reverse('issues_preview_category', args=[sk, category.slug]))
            self.assertEqual(response.status_code, 200)
            # Gets current issue object
            # Populated by critica.context_processors.current_issue
            current_issue = response.context[0]['current_issue']
            self.assert_(current_issue)
            # Should use the good template and we must be in the preview mode
            self.assertTemplateUsed(response, 'front/category.html')
            self.assertEqual(response.context[0]['is_current'], False)
            self.assertEqual(response.context[0]['is_preview'], True)
            self.assertEqual(response.context[0]['is_archive'], False)
            
    def test_preview_regions(self):
        """
        Tests issue preview for Regions category.
        
        """
        # Get issue secret key
        sk = self._get_issue_key()
        # Should return 200
        response = self.client.get(reverse('issues_preview_category_regions', args=[sk]))
        self.assertEqual(response.status_code, 200)
        # Gets current issue object
        # Populated by critica.context_processors.current_issue
        current_issue = response.context[0]['current_issue']
        self.assert_(current_issue)
        # Should use the good template and we must be in the preview mode
        self.assertTemplateUsed(response, 'front/regions.html')
        self.assertEqual(response.context[0]['is_current'], False)
        self.assertEqual(response.context[0]['is_preview'], True)
        self.assertEqual(response.context[0]['is_archive'], False) 


    def test_preview_voyages(self):
        """
        Tests issue preview Voyages category.
        
        """
        # Get issue secret key
        sk = self._get_issue_key()
        # Should return 200
        response = self.client.get(reverse('issues_preview_category_voyages', args=[sk]))
        self.assertEqual(response.status_code, 200)
        # Should use the good template and we must be in the preview mode
        self.assertTemplateUsed(response, 'front/voyages.html')
        self.assertEqual(response.context[0]['is_current'], False)
        self.assertEqual(response.context[0]['is_preview'], True)
        self.assertEqual(response.context[0]['is_archive'], False)
        
        
    def test_preview_epicurien(self):
        """
        Tests issue preview Epicurien category.
        
        """
        # Get issue secret key
        sk = self._get_issue_key()
        # Should return 200
        response = self.client.get(reverse('issues_preview_category_epicurien', args=[sk]))
        self.assertEqual(response.status_code, 200)
        # Should use the good template and we must be in the preview mode
        self.assertTemplateUsed(response, 'front/epicurien.html')
        self.assertEqual(response.context[0]['is_current'], False)
        self.assertEqual(response.context[0]['is_preview'], True)
        self.assertEqual(response.context[0]['is_archive'], False)
        

    def test_preview_anger(self):
        """
        Tests issue preview Anger category.
        
        """
        # Get issue secret key
        sk = self._get_issue_key()
        # Should return 200
        response = self.client.get(reverse('issues_preview_category_anger', args=[sk]))
        self.assertEqual(response.status_code, 200)
        # Should use the good template and we must be in the preview mode
        self.assertTemplateUsed(response, 'front/anger.html')
        self.assertEqual(response.context[0]['is_current'], False)
        self.assertEqual(response.context[0]['is_preview'], True)
        self.assertEqual(response.context[0]['is_archive'], False)


