# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.voyages`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import BaseArticle
from critica.apps.voyages.managers import PublishedArticleManager


class VoyagesArticle(BaseArticle):
    """
    Voyages article category: article.
    
    Database table name: ``voyages_article``.
    
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
            Manager: critica.apps.voyages.managers.PublishedArticleManager()
    
    """
    localization = models.CharField(_('localization'), max_length=255, db_index=True, help_text=_('Please, enter the localization in this format: city, country (e.g. Paris, France).'))
    
    objects = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'voyages_article'
        verbose_name = _('article voyage')
        verbose_name_plural = _('articles voyage')
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Auto-save category
        * Save article
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='voyages')
        self.category = category
        super(VoyagesArticle, self).save()


