# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.articles_voyages`` application.

"""
from django.db import models
from critica.apps.issues import choices as issues_choices


class PublishedArticleVoyageManager(models.Manager):
    """
    Published articles.
    
    """
    def get_query_set(self):
        """
        By default, returns only ready to publish and not reserved articles
        from complete issues.
        
        """
        return super(PublishedArticleVoyageManager, self).get_query_set().filter(
            issues__status=issues_choices.ISSUE_STATUS_COMPLETE, 
            is_ready_to_publish=True,
            is_reserved=False,
        )


