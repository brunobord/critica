# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.notes`` application.

"""
import datetime
from tagging.fields import TagField

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models import permalink

from critica.apps.notes.managers import NotePublishedManager
from critica.apps.notes.managers import NotePreviewManager
from critica.apps.notes import choices


# Types
# ------------------------------------------------------------------------------
class BaseNoteType(models.Model):
    """
    Base note type.
    
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
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.name)
        super(BaseNoteType, self).save()


class NoteType(BaseNoteType):
    """
    Generic note type.
    
    """
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table            = 'notes_notetype'
        verbose_name        = _('note type')
        verbose_name_plural = _('note types')


# Notes
# ------------------------------------------------------------------------------
class BaseNote(models.Model):
    """
    Base note

    """
    author              = models.ForeignKey('auth.User', verbose_name=_('author'), help_text=_('Please, select an author for this note.'))
    author_nickname     = models.ForeignKey('users.UserNickname', verbose_name=_('author nickname'), null=True, blank=True, help_text=_('If you want to sign this note under a nickname, please select one in the list. If you do not select a nickname, your signature will be your full name.'))
    title               = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug                = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    category            = models.ForeignKey('categories.Category', verbose_name=_('category'), null=True, blank=True, help_text=_('Please, select a category for this note.'))
    tags                = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    issues              = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues.'))
    view_count          = models.IntegerField(_('view count'), null=True, blank=True, default=0, editable=False)
    creation_date       = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date   = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date    = models.DateField(_('publication date'), null=True, blank=True, db_index=True, help_text=_("Don't forget to adjust the publication date."))
    opinion             = models.IntegerField(_('opinion'), choices=choices.OPINION_CHOICES, null=True, blank=True, db_index=True)
    is_featured         = models.BooleanField(_('featured'), default=False, db_index=True, help_text=_('Is featured?'))
    is_ready_to_publish = models.BooleanField(_('ready to publish'), default=False, db_index=True, help_text=_('Is ready to be publish?'))
    is_reserved         = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is reserved?'))
    content             = models.TextField(_('content'))

    objects   = models.Manager()
    published = NotePublishedManager()
    preview   = NotePreviewManager()


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


    def get_absolute_url(self):
        return '/%s/' % self.category.slug
        
        
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.title)
        super(BaseNote, self).save()



class Note(BaseNote):
    """
    Generic note.
    
    """
    type = models.ForeignKey('notes.NoteType', verbose_name=_('type'), help_text=_('Please, select a note type.'))
    
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table            = 'notes_note'
        verbose_name        = _('note')
        verbose_name_plural = _('notes')


