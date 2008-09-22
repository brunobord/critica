# -*- coding: utf-8 -*-
""" 
Models of ``critica.apps.users`` application. 

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """
    User profile.
    
    Database table name: ``users.userprofile``.
    
    A user profile is composed of::
    
        user
            * ForeignKey: django.contrib.auth.models.User
            * The user
            * Must be unique
            * Required

    Indexes::
    
        * user
        
    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    user = models.ForeignKey('auth.User', verbose_name=_('user'), unique=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.user
        
    def get_initials(self):
        """
        Returns user initials.
        
        """
        return u'%s.%s.' % (self.user.first_name[0], self.user.last_name[0])

        
class UserNickname(models.Model):
    """
    User nickname.
    
    Database table name: ``users_usernickname``.
    
    A user nickname is composed of::
    
        user
            * ForeignKey: django.contrib.auth.models.User
            * The user
            * Required
            
        nickname
            * CharField
            * 255 characters max.
            * The user nickname
            * Must be unique
            * Required

    Indexes::
    
        * user
        * nickname
        
    Managers::
    
        objects
            Default manager: models.Manager()
            
    """
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('user nickname')
        verbose_name_plural = _('user nicknames')
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s: %s' % (self.user, self.nickname)




