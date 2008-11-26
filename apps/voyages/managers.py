# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.voyages`` application.

"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class VoyagesArticleManager(models.Manager):
    """ 
    Base Manager. 
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(VoyagesArticleManager, self).get_query_set()

    def issue_article(self, issue_id):
        """
        Returns article of a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id)
        qs = qs.order_by('-publication_date')
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs

    def latest(self, limit=5, excluded_obj=None):
        """
        Returns the latest articles for archives.
        
        """
        qs = self.get_query_set()
        if excluded_obj:
            if hasattr(excluded_obj, 'id'):
                qs = qs.exclude(id=excluded_obj.id)
        qs.query.group_by = ['title']
        return qs[:limit]


class VoyagesArticlePublishedManager(VoyagesArticleManager):
    """
    Published Articles Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(VoyagesArticlePublishedManager, self).get_query_set().filter(
            is_ready_to_publish=True,
            is_reserved=False)
    
    
class VoyagesArticlePreviewManager(VoyagesArticleManager):
    """
    Preview Articles Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(VoyagesArticlePreviewManager, self).get_query_set().filter(is_reserved=False)
        

