# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.regions`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.notes.models import BaseNoteType, BaseNote
from critica.apps.regions.managers import PublishedNoteManager


class Region(BaseNoteType):
    """
    Region.
    
    Database table name: ``regions_region``.
    
    Fields::
    
        See BaseNoteType.
            
    Indexes::
    
        See BaseNoteType.
        
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
    
    """
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'regions_region'
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class FeaturedRegion(models.Model):
    """
    Featured region.
    
    Database table name: ``regions_featuredregion``.
    
    Fields::
    
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        region
            * ForeignKey: critica.apps.regions.models.Region
            * The region
            * Required

    Indexes::
    
        * issue
        * region

    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    region = models.ForeignKey('regions.Region', verbose_name=_('region'))
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('featured region')
        verbose_name_plural = _('featured regions')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s' % (self.issue, self.region)


class RegionNote(BaseNote):
    """
    Region note.
    
    Database table name: ``regions_note``.
    
    Fields::
    
        See BaseNote. And below.
    
        region
            * ForeignKey: critica.apps.regions.models.Region
            * The region
            * Required

    Indexes::
    
        See BaseNote and below.
        
        * region
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
            
        published
            Retrieves only published region notes. 
            Manager: critica.apps.regions.managers.PublishedNoteManager()  
    
    """
    region = models.ForeignKey('regions.Region', verbose_name=_('region'), help_text=_('Please, select a region.'))

    objects = models.Manager()
    published = PublishedNoteManager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'regions_note'
        verbose_name = _('region note')
        verbose_name_plural = _('region notes')
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Auto-save category
        * Save article
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='regions')
        self.category = category
        super(RegionNote, self).save()

