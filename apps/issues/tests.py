# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.issues`` application.

"""
import datetime
from django.test import TestCase
from apps.issues.models import Issue
from apps.positions.models import CategoryPosition, NoteTypePosition
from apps.categories.models import Category
from apps.notes.models import NoteType
from apps.positions import settings as positions_settings


class IssueTestCase(TestCase):
    """
    Issue test case.
    
    """
    
    def test_create_issue(self):
        """
        Tests issue creation.
        
        When a new issue is created, category and note type positions are
        automatically created. This test checks if all positions are correctly
        created.
        
        """
        issue = Issue(number=100, publication_date=datetime.date.today())
        issue.save()
        # Check the category position
        for slug in positions_settings.CATEGORY_DEFAULT_ORDER:
            category = Category.objects.get(slug=slug)
            positions = CategoryPosition.objects.filter(issue=issue, category=category)
            self.assertEquals(len(positions), 1)
            if slug in positions_settings.CATEGORY_DEFAULT_POSITION:
                self.assertEquals(positions[0].position, positions_settings.CATEGORY_DEFAULT_POSITION[slug])
        # Check the note type position
        categories = Category.objects.exclude(slug__in=positions_settings.EXCLUDED_CATEGORIES)
        for category in categories:
            for slug in positions_settings.NOTE_TYPE_DEFAULT_ORDER:
                note_type = NoteType.objects.get(slug=slug)
                positions = NoteTypePosition.objects.filter(issue=issue, category=category, type=note_type)
                self.assertEquals(len(positions), 1)
                if slug in positions_settings.NOTE_TYPE_DEFAULT_POSITION:
                    self.assertEquals(positions[0].position, positions_settings.NOTE_TYPE_DEFAULT_POSITION[slug])
                
