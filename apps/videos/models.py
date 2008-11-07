# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.video`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from critica.apps.utils.widgets import resize_widget
from critica.apps.videos.managers import VideoPublishedManager

class Video(models.Model):
    """
    Video.
    
    """
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    issues = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues to associate to this video.'))
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this video.'), unique=True)
    widget = models.TextField(_('widget'), help_text=_('Please, copy-paste the widget here. Do not modify it.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    is_ready_to_publish = models.BooleanField(_('ready to publish'), default=False, db_index=True, help_text=_('Is ready to be published?'))
    is_reserved = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is reserved?'))
    
    objects = models.Manager()
    published = VideoPublishedManager()
    
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
        Object pre-saving / post-saving operations.
        
        """
        new_widget = resize_widget(self.widget)
        self.widget = new_widget
        super(Video, self).save()

