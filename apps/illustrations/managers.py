# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.illustrations`` application.

"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class IllustrationOfTheDayManager(models.Manager):
    """ 
    Base Manager. 
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(IllustrationOfTheDayManager, self).get_query_set()

    def issue_illustration(self, issue_id):
        """
        Returns illustration of a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id)
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs
