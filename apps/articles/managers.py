# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.articles`` application.

"""
from django.db import models


class ArticlePreviewManager(models.Manager):
    """
    Article manager for preview mode.
    
    """
    
    def get_query_set(self):
        """
        Default QuerySet.
        
        """
        return super(ArticlePreviewManager, self).get_query_set().filter(is_reserved=False)



class ArticlePublishedManager(models.Manager):
    """
    Article manager that returns only published objects.
    
    """
    
    def get_query_set(self):
        """
        Default QuerySet.
        
        """
        return super(ArticlePublishedManager, self).get_query_set().filter(
            issues__is_published=True, 
            is_ready_to_publish=True,
            is_reserved=False)



