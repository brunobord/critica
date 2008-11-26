# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.regions`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from critica.apps.notes.models import BaseNoteType
from critica.apps.notes.models import BaseNote
from critica.apps.regions.managers import RegionNotePublishedManager
from critica.apps.regions.managers import RegionNotePreviewManager


class Region(BaseNoteType):
    """
    Region.
    
    """
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table            = 'regions_region'
        verbose_name        = _('region')
        verbose_name_plural = _('regions')


class FeaturedRegion(models.Model):
    """
    Featured region.

    """
    issue  = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    region = models.ForeignKey('regions.Region', verbose_name=_('region'))
    
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
    
    """
    region = models.ForeignKey('regions.Region', verbose_name=_('region'), help_text=_('Please, select a region.'))

    published = RegionNotePublishedManager()
    preview   = RegionNotePreviewManager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table            = 'regions_note'
        verbose_name        = _('region note')
        verbose_name_plural = _('region notes')

    @permalink
    def get_absolute_url(self):
        """
        Returns absolute URL.
        
        """
        return ('category_regions', (), {})
        
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='regions')
        self.category = category
        super(RegionNote, self).save()


