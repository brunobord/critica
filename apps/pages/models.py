# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.pages`` application.

"""
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.pages.managers import PublishedPageManager


class Page(models.Model):
    """
    Page.

    """
    author            = models.ForeignKey('auth.User', verbose_name=_('author'))
    title             = models.CharField(_('title'), max_length=255)
    slug              = models.SlugField(_('slug'), max_length=255, unique=True, editable=False)
    creation_date     = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    is_published      = models.BooleanField(_('published'), default=False, db_index=True)
    content           = models.TextField(_('content'))

    objects   = models.Manager()
    published = PublishedPageManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('page')
        verbose_name_plural = _('pages')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.title

    def author_full_name(self):
        """
        Returns author full name.
        
        """
        return self.author.get_full_name()
    author_full_name.short_description = _('author')

    @permalink
    def get_absolute_url(self):
        """ 
        Returns page's absolute URL. 
        
        """
        return ('pages_page', (), {
            'slug': self.slug,
        })

    def save(self):
        """ 
        Object pre-saving / post-saving operations. 
        
        """
        self.slug = slugify(self.title)
        super(Page, self).save()


