# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.categories`` application.

"""
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.categories import choices
from critica.apps.categories import settings as categories_settings


class Category(models.Model):
    """
    Category.
    
    Database table name: ``categories_category``.
    
    A category is composed of::
    
        name
            * CharField
            * 255 characters max.
            * The category name
            * Required
            
        slug
            * SlugField
            * 255 characters max.
            * The category slug (URL)
            * Must be unique
            * No editable
            * Required
            
        description
            * CharField
            * 255 characters max.
            * The category description
            * Optional (can be blank)
            
        image
            * ImageField (critica.apps.categories.settings.IMAGE_UPLOAD_PATH)
            * The default category illustration
            * 200 characters max.
            * Required
            
        image_credits
            * CharField
            * 100 characters max.
            * The default category illustration credits
            * default value: all rights reserved
            * Required
            
        image_legend
            * CharField
            * 100 characters max.
            * The default category illustration legend
            * Required
            
        creation_date
            * DateTimeField
            * The category creation date
            * auto_now_add
            * No editable
            * Required
            
        modification_date
            * DateTimeField
            * The category modification date
            * auto_now
            * No editable
            * Required

    Indexes::
    
        * slug
        * position_on_page

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('As short as possible.'))
    slug = models.SlugField(_('URL'), max_length=255, blank=True, unique=True, editable=False)
    description = models.CharField(_('description'), max_length=255, blank=True, help_text=_('A short description of the category. It will not be displayed on the website.'))
    image = models.ImageField(upload_to=categories_settings.IMAGE_UPLOAD_PATH, max_length=200, help_text=_('Please, upload an image for this category (it will be used as default category illustration).'))
    image_credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    image_legend = models.CharField(_('legend'), max_length=100, blank=True, help_text=_('100 characters max.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name
    
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from title
        * Save category
        
        """
        self.slug = slugify(self.name)
        super(Category, self).save()
        

class CategoryPosition(models.Model):
    """
    Category position.
    
    Database table name: ``categories_category_position``.
    
    A category position is composed of::
    
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Required
            
        position
            * IntegerField
            * The category position on the cover
            * choices: critica.apps.categories.choices.POSITION_CHOICES
            * Must be unique
            * Required

    Indexes::
    
        * issue
        * category
        * position

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    position = models.IntegerField(_('position'), choices=choices.POSITION_CHOICES, null=True, blank=True, db_index=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('category position')
        verbose_name_plural = _('category positions')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s -- %s' % (self.issue, self.category, self.position)


