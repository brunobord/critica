# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.positions`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


# Positions
# ------------------------------------------------------------------------------
class CategoryPosition(models.Model):
    """
    Category position.
    
    Database table name: ``positions_categoryposition``.
    
    Fields::
    
        name
            * CharField
            * 255 characters max.
            * The category position name
            * Must be unique
            * Required
            
        slug
            * SlugField
            * 255 characters max.
            * The category position slug (used for CSS id / classes)
            * No editable
            * Optional (can be blank)
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
            
    Indexes::
    
        * name
        * slug
    
    """
    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)

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
        return u'%s' % (self.name)

    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from name
        * Save category position
        
        """
        self.slug = slugify(self.name)
        super(CategoryPosition, self).save()


class NotePosition(models.Model):
    """
    Note position.
    
    Database table name: ``positions_noteposition``.
    
    Fields::
    
        name
            * CharField
            * 255 characters max.
            * The note position name
            * Must be unique
            * Required
            
        slug
            * SlugField
            * 255 characters max.
            * The note position slug (used for CSS id / classes)
            * No editable
            * Optional (can be blank)
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
            
    Indexes::
    
        * name
        * slug
    
    """
    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)

    objects = models.Manager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('note position')
        verbose_name_plural = _('note positions')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % (self.name)

    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from name
        * Save note position
        
        """
        self.slug = slugify(self.name)
        super(NotePosition, self).save()


# Default positions
# ------------------------------------------------------------------------------
class DefaultCategoryPosition(models.Model):
    """
    Default category position.
    
    Database table name: ``positions_defaultcategoryposition``.
    
    Fields::
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Must be unique
            * Required
            
        position
            * ForeignKey: critica.apps.positions.models.CategoryPosition
            * The category position
            * Required

    Managers::
    
        objects
            Default manager: models.Manager()
            
    Indexes::
    
        * category
        * position
        * category / position
    
    """
    category = models.ForeignKey('categories.Category', verbose_name=_('category'), unique=True)
    position = models.ForeignKey('positions.CategoryPosition', verbose_name=_('position'), null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('default category position')
        verbose_name_plural = _('default category positions')
        unique_together = (('category', 'position'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s' % (self.category, self.position)


class DefaultNotePosition(models.Model):
    """
    Default note position.
    
    Database table name: ``positions_defaultnoteposition``.
    
    Fields::
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Required

        type
            * ForeignKey: critica.apps.notes.models.NoteType
            * The note type
            * Required
            
        position
            * ForeignKey: critica.apps.positions.models.NotePosition
            * The default category position
            * Must be unique
            * Required

    Managers::
    
        objects
            Default manager: models.Manager()

    Indexes::
    
        * category
        * position
        * category / type / position

    """
    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    type = models.ForeignKey('notes.NoteType', verbose_name=_('type'))
    position = models.ForeignKey('positions.NotePosition', verbose_name=_('position'), null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('default note position')
        verbose_name_plural = _('default note positions')
        unique_together = (('category', 'type', 'position'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s' % (self.category, self.position)


# Issue positions
# ------------------------------------------------------------------------------
class IssueCategoryPosition(models.Model):
    """
    Issue category position.
    
    Database table name: ``positions_issuecategoryposition``.
    
    Fields::
    
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Required
            
        position
            * ForeignKey: critica.apps.positions.models.CategoryPosition
            * The category position
            * Required

    Indexes::
    
        * issue
        * category
        * position
        * issue / category / position

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    position = models.ForeignKey('positions.CategoryPosition', null=True, blank=True, db_index=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('issue category position')
        verbose_name_plural = _('issue category positions')
        unique_together = (('issue', 'category', 'position'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s -- %s' % (self.issue, self.category, self.position)


class IssueNotePosition(models.Model):
    """
    Issue note position.
    
    Database table name: ``notes_issuenoteposition``.
    
    Fields::
    
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
            * ForeignKey: critica.apps.positions.models.NotePosition
            * The note position
            * Optional (can be blank)

    Indexes::
    
        * issue
        * type
        * position
        * issue / category / type / position

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    type = models.ForeignKey('notes.NoteType', verbose_name=_('type'))
    position = models.ForeignKey('positions.NotePosition', verbose_name=_('position'), null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('issue note position')
        verbose_name_plural = _('issue note positions')
        unique_together = (('issue', 'category', 'type', 'position'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s -- %s -- %s' % (self.issue, self.category, self.type, self.position)
        

