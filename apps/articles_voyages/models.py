# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.articles_voyages`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import BaseArticle
from critica.apps.articles_voyages.managers import PublishedArticleVoyageManager


class ArticleVoyage(BaseArticle):
    """
    Article Voyage.
    
    Database table name: ``articles_voyages_articlevoyage``.
    
    Fields::
    
        See BaseArticle. And below.
        
        localization
            * CharField
            * 255 characters max.
            * The localization
            * Required
            
    Indexes::
    
        See BaseArticle. And below.
        
        * localization
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
        
        published
            Only returns ready to publish articles.
            Manager: critica.apps.articles_voyages.managers.PublishedArticleVoyageManager()
    
    Permissions::

        can_feature_article
            Can feature an article

        can_reserve_article
            Can reserve an article
            
        can_publish_article
            Can publish an illustration
    
    """
    localization = models.CharField(_('localization'), max_length=255, db_index=True, help_text=_('Please, enter the localization in this format: city, country (e.g. Paris, France).'))
    
    objects = models.Manager()
    published = PublishedArticleVoyageManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'articles_voyages_articlevoyage'
        verbose_name = _('article voyage')
        verbose_name_plural = _('articles voyage')
        permissions = (
            ('can_feature_article', 'Can feature an article'),
            ('can_reserve_article', 'Can reserve an article'),
            ('can_publish_article', 'Can publish an article'),
        )
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Auto-save category
        * Save article
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='voyages')
        self.category = category
        super(ArticleVoyage, self).save()


