# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.newsletter`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscriber(models.Model):
    """
    Newsletter subscriber
    
    """
    first_name        = models.CharField(_('first name'), max_length=255, null=True, blank=True)
    last_name         = models.CharField(_('last name'), max_length=255, null=True, blank=True)
    email             = models.EmailField(_('email'), max_length=255, unique=True) 
    zip_code          = models.CharField(_('zip code'), max_length=5, null=True, blank=True)
    registration_date = models.DateField(_('registration date'), auto_now_add=True) 

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('subscriber')
        verbose_name_plural = _('subscribers')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s %s' % (self.first_name, self.last_name)
