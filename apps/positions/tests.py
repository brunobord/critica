# -*- coding: utf-8 -*-
""""
Tests of ``critica.apps.positions`` application.

"""
from django.test import TestCase
from apps.positions import settings as positions_settings


class SettingsTestCase(TestCase):
    """
    Application settings test case.
    
    """
    
    def test_settings(self):
        """
        Tests lists and dictionaries of settings.py.
        
        """
        # Categories
        self.assertTrue(isinstance(positions_settings.CATEGORY_DEFAULT_ORDER, list))
        self.assertTrue(len(positions_settings.CATEGORY_DEFAULT_ORDER) > 0)
        self.assertTrue(isinstance(positions_settings.CATEGORY_DEFAULT_POSITION, dict))
        self.assertTrue(len(positions_settings.CATEGORY_DEFAULT_POSITION) > 0)
        # Excluded categories
        self.assertTrue(isinstance(positions_settings.EXCLUDED_CATEGORIES, list))
        self.assertTrue(len(positions_settings.EXCLUDED_CATEGORIES) > 0)
        # Note types
        self.assertTrue(isinstance(positions_settings.NOTE_TYPE_DEFAULT_ORDER, list))
        self.assertTrue(len(positions_settings.NOTE_TYPE_DEFAULT_ORDER) > 0)
        self.assertTrue(isinstance(positions_settings.NOTE_TYPE_DEFAULT_POSITION, dict))
        self.assertTrue(len(positions_settings.NOTE_TYPE_DEFAULT_POSITION) > 0)
        
