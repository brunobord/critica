# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.notes`` application.

"""
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.notes import choices
from critica.apps.articles.models import BaseArticle


class BaseNoteType(models.Model):
    """
    Base note type.
    
    This is an abstract class.
    
    A note type is composed of::
    
        name
            * CharField
            * 255 characters max.
            * Required
        
        slug
            * SlugField
            * 255 characters max.
            * The region type slug (can be used for CSS or later for URLs) 
            * Must be unique
            * No editable
            * Required
            
    Indexes::
    
        * slug
        
    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        abstract = True
        
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
        super(BaseNoteType, self).save()


class NoteType(BaseNoteType):
    """
    Generic note type.
    
    Database table name: ``notes_note_type``.
    
    A generic note type is composed of::
    
        Inherits from critica.apps.notes.models.BaseNoteType.
        So, all fields of this abstract class and fields below.
            
        position_on_page
            * IntegerField
            * choices: critica.apps.notes.choices.NOTE_TYPE_POSITION_CHOICES
            * Required
            
    Indexes::
    
        BaseNoteType indexes and below.
        
        * position_on_page
        
    Managers::
    
        See BaseNoteType.
    
    """
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'notes_note_type'
        verbose_name = _('note type')
        verbose_name_plural = _('note types')


class NoteTypePosition(models.Model):
    """
    NOte type position.
    
    Database table name: ``notes_note_type_position``.
    
    A note type position is composed of::
    
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        type
            * ForeignKey: critica.apps.notes.models.NoteType
            * The note type
            * Required
            
        position
            * IntegerField
            * The category position on the cover
            * choices: critica.apps.categories.choices.POSITION_CHOICES
            * Must be unique
            * Required

    Indexes::
    
        * issue
        * type
        * position

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    type = models.ForeignKey('categories.Category', verbose_name=_('category'))
    position = models.IntegerField(_('position'), choices=choices.NOTE_TYPE_POSITION_CHOICES, unique=True, db_index=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('note type position')
        verbose_name_plural = _('note type positions')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s -- %s' % (self.issue, self.type, self.position)


class BaseNote(BaseArticle):
    """
    Base note.
    
    This is an abstract class.
    
    A note is composed of::
    
        Inherits from critica.apps.articles.models.BaseArticle.
        So, all fields of this abstract class.

    Indexes::
    
        BaseArticle indexes.
            
    Managers::
    
        See BaseArticle.
        
    Permissions::
            
        can_reserve_note
            Can reserve a note
            
        can_feature_note
            Can feature a note
    
    """
    class Meta:
        abstract = True
        permissions = (
            ('can_reserve_note', 'Can reserve a note'),
            ('can_feature_note', 'Can feature a note'),
        )


class Note(BaseNote):
    """
    Generic note.
    
    Database table name: ``notes_note``.
    
    A note is composed of::
    
        Inherits from critica.apps.notes.models.BaseNote.
        So, all fields of this abstract class and fields below.
    
        type
            * ForeignKey: critica.apps.notes.models.NoteType
            * The general note type
            * Required

    Indexes::
    
        BaseNote indexes and below.
        
        * type
            
    Managers::
    
        See BaseNote.
        
    Permissions::
    
        See BaseNote.
    
    """
    type = models.ForeignKey('notes.NoteType', verbose_name=_('type'), help_text=_('Please, select a note type.'))

    class Meta:
        db_table = 'notes_note'
        verbose_name = _('note')
        verbose_name_plural = _('notes')


