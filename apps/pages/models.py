# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.pages``.

"""
from datetime import datetime
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from critica.apps.pages.managers import PageManager


class Page(models.Model):
    """
    Page.
    
    A page is composed of::
    
        title
            The page title. Max. 255 characters.
            Required.
            
        slug
            The page slug. Max. 255 characters.
            Required.
            
        author
            The page author (derived from ``django.contrib.auth.models.User``).
            
        creation_date
            The page creation date.
            
        modification_date
            The page modification date.
            
        is_published
            Is page published? Default to ``False``.
            
        content
            The page content.
            
    Managers::
        
        objects
            All objects.
            
        published
            Published pages.
    
    """
    title             = models.CharField(_('title'), max_length=255)
    slug              = models.SlugField(_('slug'), max_length=255, unique=True)
    author            = models.ForeignKey(User, verbose_name=_('author'))
    creation_date     = models.DateTimeField(_('creation date'), null=True, blank=True)
    modification_date = models.DateTimeField(_('modification date'), null=True, blank=True)
    is_published      = models.BooleanField(_('published'), default=False)
    content           = models.TextField(_('content'))
    
    class Meta:
        """ Model metadata. """
        verbose_name = _('page')
        verbose_name_plural = _('pages')
    
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.title
        
    @permalink
    def get_absolute_url(self):
        """ Returns page's absolute URL. """
        return ('pages_page', (), { 
            'slug': self.slug,
        })

    def save(self):
        """ Object pre-saving operations. """
        if not self.id:
            self.creation_date = datetime.now()
            self.modification_date = self.creation_date
        else:
            self.modification_date = datetime.now()
        super(Page, self).save()
    
    # Managers
    objects = models.Manager()
    published = PageManager()


