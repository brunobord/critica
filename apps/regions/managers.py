# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.regions`` application.

"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

    
class RegionNoteManager(models.Manager):
    """
    Base Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(RegionNoteManager, self).get_query_set()
        
    def get_featured(self, issue_id):
        """
        Returns featured region note for a given issue.
        
        """
        from critica.apps.regions.models import FeaturedRegion
        try:
            featured = FeaturedRegion.objects.get(issue__id=issue_id)
        except ObjectDoesNotExist:
            featured = None
        note = None
        if featured:
            note = self.get_query_set().filter(issues__id=issue_id, region=featured.region)
            note = note.order_by('-publication_date')
            try:
                note = note[0:1].get()
            except ObjectDoesNotExist:
                note = None
        return note
        
    def get_notes(self, issue_id, excluded_obj):
        """
        Returns ordered region notes.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id).order_by('region__name')
        qs = qs.exclude(id=excluded_obj.id)
        return qs

    
class RegionNotePublishedManager(RegionNoteManager):
    """
    Published Notes Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(RegionNotePublishedManager, self).get_query_set().filter(
            is_ready_to_publish=True,
            is_reserved=False)
    
    
class RegionNotePreviewManager(RegionNoteManager):
    """
    Preview Notes Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(RegionNotePreviewManager, self).get_query_set().filter(is_reserved=False)


