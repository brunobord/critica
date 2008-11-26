# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.epicurien`` application.

"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class EpicurienArticleManager(models.Manager):
    """ 
    Base Manager. 
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(EpicurienArticleManager, self).get_query_set()

    def issue_article_cotefumeurs(self, issue_id):
        """
        Returns article of "côte fumeurs" subcategory of a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id, type__slug='cote-fumeurs')
        qs = qs.order_by('-publication_date')
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs
    
    def issue_article_cotegourmets(self, issue_id):
        """
        Returns article of "côte gourmets" subcategory of a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id, type__slug='cote-gourmets')
        qs = qs.order_by('-publication_date')
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs
    
    def issue_article_cotebar(self, issue_id):
        """
        Returns article of "côte bar" subcategory of a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id, type__slug='cote-bar')
        qs = qs.order_by('-publication_date')
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs

    def latest(self, type_id=None, limit=5, excluded_obj=None):
        """
        Returns the latest articles for archives.
        
        """
        qs = self.get_query_set()
        if excluded_obj:
            if hasattr(excluded_obj, 'id'):
                qs = qs.exclude(id=excluded_obj.id)
        qs = qs.filter(type__id=type_id)
        qs.query.group_by = ['title']
        return qs[:limit]


class EpicurienArticlePublishedManager(EpicurienArticleManager):
    """
    Published Articles Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(EpicurienArticlePublishedManager, self).get_query_set().filter(
            is_ready_to_publish=True,
            is_reserved=False)


class EpicurienArticlePreviewManager(EpicurienArticleManager):
    """
    Preview Articles Manager.
    
    """
    def get_query_set(self):
        """
        Default QuerySet.
        
        """
        return super(EpicurienArticleManager, self).get_query_set().filter(is_reserved=False)


