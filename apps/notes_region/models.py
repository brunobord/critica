# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.notes_region`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.notes.models import BaseNoteType, BaseNote
from critica.apps.notes_region.managers import PublishedNoteRegionManager


class NoteTypeRegion(BaseNoteType):
    """
    Region note type.
    
    Database table name: ``notes_region_notetyperegion``.
    
    A region note type is composed of::
    
        Inherits from critica.apps.notes.models.BaseNoteType.
        So, all fields of this abstract class.
            
    Indexes::
    
        See BaseNoteType.
        
    Managers::
    
        See BaseNoteType.
    
    """
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'notes_region_notetyperegion'
        verbose_name = _('region note type')
        verbose_name_plural = _('region note types')


class NoteRegionFeatured(models.Model):
    """
    Featured note region.
    
    Database table name: ``notes_region_noteregionfeatured``.
    
    A featured note region is composed of::
    
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        type
            * ForeignKey: critica.apps.notes_region.models.NoteTypeRegion
            * The region type
            * Required

    Indexes::
    
        * issue
        * type

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    type = models.ForeignKey('notes_region.NoteTypeRegion', verbose_name=_('type'))
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('featured region note')
        verbose_name_plural = _('featured region notes')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s' % (self.issue, self.type)


class NoteRegion(BaseNote):
    """
    Region note.
    
    Database table name: ``notes_region_noteregion``.
    
    A note is composed of::
    
        Inherits from critica.apps.notes.models.BaseNote.
        So, all fields of this abstract class and fields below.
    
        type
            * ForeignKey: critica.apps.notes_region.models.NoteTypeRegion
            * The region note type
            * Required

    Indexes::
    
        BaseNote indexes and below.
        
        * type
            
    Managers::
    
        objects
            Default manager: models.Manager()
            
        published
            Retrieves only published region notes.   
        
    Permissions::
    
        See BaseNote.
    
    """
    type = models.ForeignKey('notes_region.NoteTypeRegion', verbose_name=_('type'), help_text=_('Please, select a note type.'))

    objects = models.Manager()
    published = PublishedNoteRegionManager()
    
    class Meta:
        db_table = 'notes_region_noteregion'
        verbose_name = _('region note')
        verbose_name_plural = _('region notes')



