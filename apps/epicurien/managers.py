# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.epicurien`` application.

"""
from django.db import models
from critica.apps.issues import choices as issues_choices


class PublishedArticleManager(models.Manager):
    """
    Published Epicurien articles.
    
    """
    def get_query_set(self):
        """
        By default, returns only ready to publish and not reserved articles
        from complete issues.
        
        """
        return super(PublishedArticleManager, self).get_query_set().filter(
            issues__status=issues_choices.ISSUE_STATUS_COMPLETE, 
            is_ready_to_publish=True,
            is_reserved=False
        )

