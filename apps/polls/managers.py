# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.polls`` application.

"""
from django.db import models


class PollPublishedManager(models.Manager):
    """
    Published poll manager.
    
    """
    def get_query_set(self):
        """
        Default QuerySet.
        
        """
        return super(PollPublishedManager, self).get_query_set().filter(is_published=True)
