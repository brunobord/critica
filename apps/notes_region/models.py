# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.notes_region`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.notes.models import BaseNoteType, BaseNote
from critica.apps.notes_region.managers import PublishedNoteRegionManager


# Types
# ------------------------------------------------------------------------------
class NoteTypeRegion(BaseNoteType):
    """
    Region note type.
    
    Database table name: ``notes_region_notetyperegion``.
    
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
        db_table = 'notes_region_notetyperegion'
        verbose_name = _('region note type')
        verbose_name_plural = _('region note types')


class NoteRegionFeatured(models.Model):
    """
    Featured note region.
    
    Database table name: ``notes_region_noteregionfeatured``.
    
    Fields::
    
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
            Default manager.
            Manager: models.Manager()
    
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


# Notes
# ------------------------------------------------------------------------------
class NoteRegion(BaseNote):
    """
    Region note.
    
    Database table name: ``notes_region_noteregion``.
    
    Fields::
    
        See BaseNote. And below.
    
        type
            * ForeignKey: critica.apps.notes_region.models.NoteTypeRegion
            * The region note type
            * Required

    Indexes::
    
        See BaseNote and below.
        
        * type
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
            
        published
            Retrieves only published region notes. 
            Manager: critica.apps.notes_region.managers.PublishedNoteRegionManager()  
        
    Permissions::
    
        can_feature_note
            Can feature a note
            
        can_reserve_note
            Can reserve a note
            
        can_publish_note
            Can publish a note
    
    """
    type = models.ForeignKey('notes_region.NoteTypeRegion', verbose_name=_('type'), help_text=_('Please, select a note type.'))

    objects = models.Manager()
    published = PublishedNoteRegionManager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'notes_region_noteregion'
        verbose_name = _('region note')
        verbose_name_plural = _('region notes')
        permissions = (
            ('can_feature_note', 'Can feature a note'),
            ('can_reserve_note', 'Can reserve a note'),
            ('can_publish_note', 'Can publish a note'),
        )

