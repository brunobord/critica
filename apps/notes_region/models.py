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
    
    Database table name: ``notes_note_type_region``.
    
    A region note type is composed of::
    
        Inherits from critica.apps.notes.models.BaseNoteType.
        So, all fields of this abstract class and fields below.
            
        is_featured
            * BooleanField
            * Default: False
            * Is region type featured?
            * Required
            
    Indexes::
    
        BaseNoteType indexes and below.
        
        * featured
        
    Managers::
    
        See BaseNoteType.
    
    """
    is_featured = models.BooleanField(_('featured'), default=False, db_index=True)
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'notes_note_type_region'
        verbose_name = _('region note type')
        verbose_name_plural = _('region note types')


class NoteRegion(BaseNote):
    """
    Region note.
    
    Database table name: ``notes_note_region``.
    
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
        db_table = 'notes_note_region'
        verbose_name = _('region note')
        verbose_name_plural = _('region notes')


