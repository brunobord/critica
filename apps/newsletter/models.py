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
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    email = models.EmailField(_('email'), max_length=255, unique=True) 
    zip_code = models.CharField(_('zip code'), max_length=5) 

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s %s' % (self.first_name, self.last_name)
