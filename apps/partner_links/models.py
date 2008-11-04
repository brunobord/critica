# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.partner_links`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PartnerLink(models.Model):
    """
    Partner Link.
    
    """
    name      = models.CharField(_('name'), max_length=255, unique=True)
    link      = models.URLField(_('URL'))
    is_active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('partner link')
        verbose_name_plural = _('partner links')
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name

