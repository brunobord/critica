# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.video`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from critica.apps.videos import choices
#from critica.apps.videos.managers import PublishedVideoManager


class Video(models.Model):
    """
    Video.
    
    Database table name: ``videos_video``.
    
    A video is composed of::
    
        submitter
            * ForeignKey: django.contrib.auth.models.User
            * User who submitted the video
            * Required
            
        name
            * CharField
            * 255 characters max.
            * The video name
            * Required

        slug
            * SlugField
            * 255 characters max.
            * The video slug (URL)
            * No editable
            * Required
            
        link
            * CharField
            * 255 characters max.
            * The video link
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
            
        status
            * IntegerField
            * Choices: critica.apps.videos.choices.STATUS_CHOICES
            * Default: critica.apps.videos.choices.STATUS_NEW
            * The video status
            * Required
    
    Indexes::
    
        * submitter
        * status
    
    Managers::
    
        objects
            Default manager: models.Manager()
            
        published
            Retrieves only published videos.
    
    """

    
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this video.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    link = models.CharField(_('link'), max_length=255, help_text=_('Please, enter the video URL.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    status = models.IntegerField(_('status'), choices=choices.STATUS_CHOICES, default=choices.STATUS_NEW, db_index=True, help_text=_('Please, select a status.'))
    
    objects = models.Manager()
#    published = PublishedVideoManager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        permissions = (
            ('can_reserve_video', 'Can reserve a video'),
            ('can_publish_video', 'Can publish a video'),
        )

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name

    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from name
        * Save video
        
        """
        self.slug = slugify(self.name)
        super(Video, self).save()


class VideoOfTheDay(Video):
    """
    Illustration of the day.
    
    Database table name: ``video_videooftheday``.
    
    An video of the day is composed of::
    
        Inherits from VideoOfTheDay.
        So, all fields of this class.
        
    Indexes::
    
        Video indexes.
            
    Managers::
    
        Video Illustration.
    
    """
    pass
    

