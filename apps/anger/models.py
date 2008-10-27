# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.anger`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import BaseArticle
from critica.apps.voyages.managers import PublishedArticleManager


class AngerArticle(BaseArticle):
    """
    Anger article category: article.
    
    Database table name: ``anger_article``.
    
    Fields::
    
        See BaseArticle.
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
        
        published
            Only returns ready to publish articles.
            Manager: critica.apps.anger.managers.PublishedArticleManager()

    Indexes::
    
        See BaseArticle.
    
    """
    objects = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'anger_article'
        verbose_name = _('article anger')
        verbose_name_plural = _('articles anger')
        
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='coup-de-gueule')
        self.category = category
        super(AngerArticle, self).save()


