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
    return 'upload/idj/%s-%s' % (instance.id, filename)


class IllustrationOfTheDay(models.Model):
    """
    Illustration of the day.
    
    """
    submitter         = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    issues            = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues to associate to this illustration.'))
    image             = models.ImageField(upload_to=get_image_path, max_length=200, help_text=_('Please, select an image to upload'))
    credits           = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend            = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    creation_date     = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    
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
        

