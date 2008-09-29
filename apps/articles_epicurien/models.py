# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.articles_epicurien`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.articles.models import BaseArticle
from critica.apps.articles_epicurien.managers import PublishedArticleEpicurienManager


class ArticleEpicurienType(models.Model):
    """
    Article 'Epicurien'.
    
    Database table name: ``articles_epicurien_articleepicurientype``.
    
    Fields::
    
        name
            * CharField
            * 255 characters max.
            * Required
        
        slug
            * SlugField
            * 255 characters max.
            * The type slug (can be used for CSS or later for URLs) 
            * Must be unique
            * No editable
            * Required
            
    Indexes::
    
        * slug
        
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
    
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('URL'), max_length=255, unique=True, blank=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('article epicurien type')
        verbose_name_plural = _('article epicurien types')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from title
        * Save note type
        
        """
        self.slug = slugify(self.name)
        super(ArticleEpicurienType, self).save()



class ArticleEpicurien(BaseArticle):
    """
    Article 'Epicurien'.
    
    Database table name: ``articles_epicurien_articleepicurien``.
    
    Fields::
    
        See BaseArticle. And fields below.
        
        type
            * ForeignKey: critica.apps.articles_epicurien.models.ArticleEpicurienType
            * The article type
            * Required
            
    Indexes::
    
        See BaseArticle. And below.
        
        * type
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
        
        published
            Only returns ready to publish articles.
            Manager: critica.apps.articles.managers.PublishedArticleEpicurienManager()
    
    Permissions::

        can_feature_article
            Can feature an article

        can_reserve_article
            Can reserve an article
            
        can_publish_article
            Can publish an illustration
    
    """
    type = models.ForeignKey('articles_epicurien.ArticleEpicurienType', verbose_name=_('type'))
    
    objects = models.Manager()
    published = PublishedArticleEpicurienManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'articles_epicurien_articleepicurien'
        verbose_name = _('article epicurien')
        verbose_name_plural = _('articles epicurien')
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
        category = Category.objects.get(slug='epicurien')
        self.category = category
        super(ArticleEpicurien, self).save()


