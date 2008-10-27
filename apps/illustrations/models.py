# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.illustrations`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.illustrations import settings as illustrations_settings


def get_image_path(instance, filename):
    """
    Dynamic image upload path.
    
    """
    return 'upload/images/idj/%s-%s' % (instance.id, filename)


class IllustrationOfTheDay(models.Model):
    """
    Illustration of the day.
    
    Database table name: ``illustrations_illustrationoftheday``.
    
    An illustration of the day is composed of::
    
        submitter
            * ForeignKey: django.contrib.auth.models.User
            * User who submitted the illustration
            * Required
            
        issues
            * ManyToManyField: critica.apps.issues.models.Issue
            * The illustration of the day issues
            * Optional (can be blank)
            
        image
            * ImageField (critica.apps.illustrations.settings.IMAGE_UPLOAD_PATH)
            * 200 characters max.
            * The illustration image file
            * Required
            
        credits
            * CharField
            * 100 characters max.
            * The illustration credits
            * Default value: all rights reserved
            * Required
            
        legend
            * CharField
            * 100 characters max.
            * The illustration legend
            * Required
            
        creation_date
            * DateTimeField
            * auto_now_add
            * The illustration creation date
            * No editable
            * Required
        
        modification_date
            * DateTimeField
            * auto_now
            * No editable
            * Required
    
    Indexes::
    
        * submitter

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    submitter         = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    issues            = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues to associate to this illustration.'))
    image             = models.ImageField(upload_to=get_image_path, max_length=200, help_text=_('Please, select an image to upload'))
    credits           = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend            = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    creation_date     = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('illustration of the day')
        verbose_name_plural = _('illustrations of the day')


    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.legend
        

