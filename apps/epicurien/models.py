# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.epicurien`` application.

"""
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.articles.models import BaseArticle


class EpicurienArticleType(models.Model):
    """
    Epicurien article type.
    
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('URL'), max_length=255, unique=True, blank=True, editable=False)
    
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
    
    def _get_type_number(self):
        """ 
        Private method that returns the type number for anchors. 
        
        """
        if self.type.id == 1:
            type_number = '#1'
        if self.type.id == 2:
            type_number = '#2'
        if self.type.id == 3:
            type_number = '#3'
        return type_number

    def get_absolute_url(self):
        """
        Returns absolute URL.
        
        """
        return '/epicurien/%s' % self._get_type_number()
        
    def get_archive_url(self):
        """
        Returns archive URL.
        
        """

        issue = self.issues.all()[0]
        return '/archives/%s/epicurien/%s' % (issue.number, self._get_type_number())
        
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='epicurien')
        self.category = category
        super(EpicurienArticle, self).save()


