# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.notes`` application.

"""
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from critica.apps.articles.models import BaseArticle
from critica.apps.notes.managers import PublishedNoteManager
from critica.apps.notes import choices


# Types
# ------------------------------------------------------------------------------
class BaseNoteType(models.Model):
    """
    Base note type.
    
    This is an abstract class.
    
    Fields::
    
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
    
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    
    
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
    
    Database table name: ``notes_notetype``.
    
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
        db_table = 'notes_notetype'
        verbose_name = _('note type')
        verbose_name_plural = _('note types')


# Notes
# ------------------------------------------------------------------------------
class BaseNote(models.Model):
    """
    Base note.
    
    This is an abstract class.
    
    Fields::
    
        author
            * ForeignKey: django.contrib.auth.models.User
            * The note author
            * Required
            
        author_nickname
            * ForeignKey: critica.apps.users.models.UserNickname
            * The author nickname
            * Optional (can be blank)
            
        title
            * CharField
            * 255 characters max.
            * The note title
            * Required
            
        slug
            * SlugField
            * 255 characters max.
            * The note slug
            * No editable
            * Optional (can be blank)
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The note category
            * Required
            
        tags
            * TagField (from tagging)
            * The note tags
            * Optional
            
        issues
            * ManyToManyField: critica.apps.issues.models.Issue
            * The note issues
            * Optional (can be blank)
            
        view_count
            * PositiveIntegerField
            * The note view count
            * No editable
            * Optional (can be blank)
            
        creation_date
            * DateTimeField
            * auto_now_add
            * The note creation date
            * Required
            
        modification_date
            * DateTimeField
            * auto_now
            * The note modification date
            * Required
            
        publication_date
            * DateField
            * The note publication date
            * Optional (can be blank)
        
        opinion
            * IntegerField
            * Choices: critica.apps.article.choices.OPINION_CHOICES
            * The note opinion flag
            * Optional (can be blank)

        is_featured
            * BooleanField
            * Default: False
            * Is note featured?
            * Required
            
        is_ready_to_publish
            * BooleanField
            * Default: False
            * Is note ready to publish?
            * Required
            
        is_reserved
            * BooleanField
            * Default: False
            * Is note reserved?
            * Required
            
        content
            * TextField
            * The note content
            * Required
            
    Indexes::
    
        * author
        * author_nickname
        * slug
        * category
        * issues
        * publication_date
        * opinion
        * is_featured
        * is_ready_to_publish
        * is_reserved

    """
    author = models.ForeignKey('auth.User', verbose_name=_('author'), help_text=_('Please, select an author for this note.'))
    author_nickname = models.ForeignKey('users.UserNickname', verbose_name=_('author nickname'), null=True, blank=True, help_text=_('If you want to sign this note under a nickname, please select one in the list. If you do not select a nickname, your signature will be your full name.'))
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    category = models.ForeignKey('categories.Category', verbose_name=_('category'), null=True, blank=True, help_text=_('Please, select a category for this note.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    issues = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues.'))
    view_count = models.IntegerField(_('view count'), null=True, blank=True, editable=False)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date = models.DateField(_('publication date'), null=True, blank=True, db_index=True, help_text=_("Don't forget to adjust the publication date."))
    opinion = models.IntegerField(_('opinion'), choices=choices.OPINION_CHOICES, null=True, blank=True, db_index=True)
    is_featured = models.BooleanField(_('featured'), default=False, db_index=True, help_text=_('Is featured?'))
    is_ready_to_publish = models.BooleanField(_('ready to publish'), default=False, db_index=True, help_text=_('Is ready to be publish?'))
    is_reserved = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is reserved?'))
    content = models.TextField(_('content'))
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        abstract = True

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u"%s" % (self.title)
    
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from title
        * Save note
        
        """
        self.slug = slugify(self.title)
        super(BaseNote, self).save()


class Note(BaseNote):
    """
    Generic note.
    
    Database table name: ``notes_note``.
    
    Fields::
    
        See BaseNote. And below.
    
        type
            * ForeignKey: critica.apps.notes.models.NoteType
            * The note type
            * Required

    Indexes::
    
        See BaseNote. And below.
        
        * type
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
            
        published
            Only returns ready to publish notes.
            Manager: critica.apps.notes.managers.PublishedNoteManager()

    Permissions::

        can_feature_note
            Can feature a note
            
        can_reserve_note
            Can reserve a note
            
        can_publish_note
            Can publish a note
    
    """
    type = models.ForeignKey('notes.NoteType', verbose_name=_('type'), help_text=_('Please, select a note type.'))
    
    objects = models.Manager()
    published = PublishedNoteManager()

    class Meta:
        db_table = 'notes_note'
        verbose_name = _('note')
        verbose_name_plural = _('notes')
        permissions = (
            ('can_feature_note', 'Can feature a note'),
            ('can_reserve_note', 'Can reserve a note'),
            ('can_publish_note', 'Can publish a note'),
        )

