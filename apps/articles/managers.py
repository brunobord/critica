# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.articles`` application.

"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class ArticleManager(models.Manager):
    """
    Base Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(ArticleManager, self).get_query_set()

    def category_article(self, issue_id, category_id):
        """
        Returns article of a given category and a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id, category__id=category_id)
        qs = qs.order_by('-publication_date')
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs


class ArticlePublishedManager(ArticleManager):
    """
    Published Articles Manager.
    
    """    
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(ArticlePublishedManager, self).get_query_set().filter(
            is_ready_to_publish=True, 
            is_reserved=False)


class ArticlePreviewManager(ArticleManager):
    """
    Preview Articles Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(ArticlePreviewManager, self).get_query_set().filter(is_reserved=False)
        

