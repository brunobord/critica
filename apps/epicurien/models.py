# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.epicurien`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.articles.models import BaseArticle


class EpicurienArticleType(models.Model):
    """
    Epicurien article type.
    
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('URL'), max_length=255, unique=True, blank=True, editable=False)
    
    objects = models.Manager()
    
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table            = 'epicurien_articletype'
        verbose_name        = _('article epicurien type')
        verbose_name_plural = _('article epicurien types')


    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name

        
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.name)
        super(Type, self).save()



class EpicurienArticle(BaseArticle):
    """
    Epicurien article.
    
    """
    type = models.ForeignKey('epicurien.EpicurienArticleType', verbose_name=_('type'))


    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table            = 'epicurien_article'
        verbose_name        = _('article epicurien')
        verbose_name_plural = _('articles epicurien')


    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='epicurien')
        self.category = category
        super(EpicurienArticle, self).save()


