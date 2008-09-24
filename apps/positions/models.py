# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.positions`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.positions import choices


class CategoryPosition(models.Model):
    """
    Category position.
    
    Database table name: ``positions_category_position``.
    
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
            * choices: critica.apps.positions.choices.CATEGORY_POSITION_CHOICES
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
    position = models.IntegerField(_('position'), choices=choices.CATEGORY_POSITION_CHOICES, null=True, blank=True, db_index=True)
    
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


class NoteTypePosition(models.Model):
    """
    NOte type position.
    
    Database table name: ``notes_notetypeposition``.
    
    A note type position is composed of::
    
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Required
        
        type
            * ForeignKey: critica.apps.notes.models.NoteType
            * The note type
            * Required
            
        position
            * IntegerField
            * The category position on the cover
            * choices: critica.apps.notes.choices.POSITION_CHOICES
            * Must be unique
            * Optional (can be blank)

    Indexes::
    
        * issue
        * type
        * position

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    type = models.ForeignKey('notes.NoteType', verbose_name=_('type'))
    position = models.IntegerField(_('position'), choices=choices.NOTE_TYPE_POSITION_CHOICES, null=True, blank=True, db_index=True)
    
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
        return u'%s -- %s -- %s -- %s' % (self.issue, self.category, self.type, self.position)
        

