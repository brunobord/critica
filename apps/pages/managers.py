# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.pages`` models.

"""
from django.db import models


class PublishedPageManager(models.Manager):
    """
    Published pages.
    
    """
    def get_query_set(self):
        """ 
        Retrieves published pages. 
        
        """
        return super(PublishedPageManager, self).get_query_set().filter(is_published=True)


