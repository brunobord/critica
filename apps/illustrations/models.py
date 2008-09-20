# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.illustrations`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.illustrations import settings as illustrations_settings


class Illustration(models.Model):
    """
    Illustration.
    
    Database table name: ``illustrations_illustration``.
    
    An illustration is composed of::
    
        submitter
            * ForeignKey: django.contrib.auth.models.User
            * User who submitted the illustration
            * Required
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The illustration category
            * Required
            
        image
            * ImageField (critica.apps.illustrations.settings.IMAGE_UPLOAD_PATH)
            * 200 characters max.
            * The illustration image file
            * Required
            
        credits
            * CharField
            * 100 characters max.
            * The illustration credits
            * Default value: all rights reserved
            * Required
            
        legend
            * CharField
            * 100 characters max.
            * The illustration legend
            * Required
            
        creation_date
            * DateTimeField
            * auto_now_add
            * The illustration creation date
            * No editable
            * Required
        
        modification_date
            * DateTimeField
            * auto_now
            * No editable
            * Required
    
    Indexes::
    
        * submitter
        * category

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'), blank=True)
    image = models.ImageField(upload_to=illustrations_settings.IMAGE_UPLOAD_PATH, max_length=200, help_text=_('Please, select an image to upload'))
    credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('illustration')
        verbose_name_plural = _('illustrations')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.legend

    def image_ld(self):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.legend)
    image_ld.allow_tags = True
    image_ld.short_description = _('Illustration')

    def category_ld(self):
        """
        Formatted category for admin list_display option.
        
        """
        return '<strong>%s</strong>' % self.category
    category_ld.allow_tags = True
    category_ld.short_description = _('Category')


