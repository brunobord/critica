# -*- coding: utf-8 -*-
""" 
Models of ``critica.apps.users`` application. 

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """
    User profile.

    """
    user = models.ForeignKey('auth.User', verbose_name=_('user'), unique=True)
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        permissions = (
            ('is_administrator', 'User is administrator'),
            ('is_editor', 'User is editor'),
            ('is_journalist', 'User is journalist'),
            ('is_advertiser', 'User is advertiser'),
        )
    
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
            
    """
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    
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


