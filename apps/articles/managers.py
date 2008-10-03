# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.articles`` application.

"""
from django.db import models


class PublishedArticleManager(models.Manager):
    """
    Published articles.
    
    """
    def get_query_set(self):
        """
        By default, returns only ready to publish and not reserved articles
        from complete issues.
        
        """
        return super(PublishedArticleManager, self).get_query_set().filter(
            issues__is_published=True, 
            is_ready_to_publish=True,
            is_reserved=False
        )

