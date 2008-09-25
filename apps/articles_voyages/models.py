# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.articles_voyage`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import Article


class ArticleVoyage(Article):
    """
    Article 'Voyage'.
    
    Database table name: ``articles_voyages_articlevoyage``.
    
    An article 'voyage' is composed of::
    
        Inherits from BaseArticle.
        So, all fields of this abstract class and fields below.
        
        localization
            * CharField
            * 255 characters max.
            * The localization
            * Required
            
    Indexes::
    
        BaseArticle indexes and below.
        
        * localization
            
    Managers::
    
        See BaseArticle.
        
    Permissions::
    
        See BaseArticle.
    
    """
    localization = models.CharField(_('localization'), max_length=255, db_index=True)
    
    objects = models.Manager()

    class Meta:
        db_table = 'articles_voyages_articlevoyage'
        verbose_name = _('article voyage')
        verbose_name_plural = _('articles voyage')
        permissions = (
            ('can_feature_article', 'Can feature an article'),
            ('can_reserve_article', 'Can reserve an article'),
            ('can_publish_article', 'Can publish an article'),
        )
        
    def save(self):
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='voyages')
        self.category = category
        super(ArticleVoyage, self).save()

