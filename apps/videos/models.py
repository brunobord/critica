# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.video`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from critica.apps.videos.utils import resize_video


class Video(models.Model):
    """
    Video.
    
    Database table name: ``videos_video``.
    
    A video is composed of::
    
        submitter
            * ForeignKey: django.contrib.auth.models.User
            * User who submitted the video
            * Required
            
        issues
            * ManyToManyField: critica.apps.issues.models.Issue
            * The video issues
            * Optional (can be blank)
            
        name
            * CharField
            * 255 characters max.
            * The video name
            * Required
            
        widget
            * TextField
            * The video widget
            * Required

        tags
            * TagField (from tagging)
            * The video tags
            * Optional
            
        creation_date
            * DateTimeField
            * auto_now_add
            * Reportage creation date
            * No editable
            * Required
            
        modification_date
            * DateTimeField
            * auto_now
            * Reportage modification date
            * No editable
            * Required
            
        is_ready_to_publish
            * BooleanField
            * Default: False
            * Is video ready to publish?
            * Required
            
        is_reserved
            * BooleanField
            * Default: False
            * Is video reserved?
            * Required
    
    Indexes::
    
        * submitter
        * issues
        * name
        * tags
        * is_ready_to_publish
        * is_reserved
    
    Managers::
    
        objects
            Default manager: models.Manager()
            
        published
            Retrieves only published videos.
    
    """
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    issues = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues to associate to this video.'))
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this video.'), unique=True)
    widget = models.TextField(_('widget'), help_text=_('Please, copy-paste the widget here. Do not modify it.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    is_ready_to_publish = models.BooleanField(_('ready to publish'), default=False, db_index=True, help_text=_('Is ready to be published?'))
    is_reserved = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is reserved?'))
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Resize video
        * Save video
        
        """
        new_widget = resize_video(self.widget)
        self.widget = new_widget
        super(Video, self).save()

