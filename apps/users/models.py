# -*- coding: utf-8 -*-
""" 
Models for ``critica.apps.users``. 

"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """ User profile. """
    user = models.ForeignKey(User, verbose_name=_('user'), unique=True)
    
    class Meta:
        permissions = (
            ('can_reserve_article', 'Can reserve an article'),
            ('can_feature_article', 'Can feature an article'),
            ('can_illustrate_article', 'Can illustrate an article'),
            ('can_position_article', 'Can position an article'),
            ('can_publish_article', 'Can publish an article'),
            ('can_publish_page', 'Can publish a page'),
        )
        
    def get_initials(self):
        """ Returns user's initials. """
        return u'%s.%s.' % (self.user.first_name[0], self.user.last_name[0])


