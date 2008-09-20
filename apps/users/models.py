# -*- coding: utf-8 -*-
""" 
Models for ``critica.apps.users``. 

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('user'), unique=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        
    def get_initials(self):
        return u'%s.%s.' % (self.user.first_name[0], self.user.last_name[0])


