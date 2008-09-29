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

    Fields::

        author
            * ForeignKey: django.contrib.auth.models.User
            * The page's author
            * Required
            
        title
            * CharField
            * 255 characters max.
            * The page's title
            * Required

        slug
            * SlugField
            * 255 characters max.
            * The page's slug
            * Must be unique
            * Required (auto-generated)

        creation_date
            * DateTimeField
            * auto_now_add
            * The page's creation date
            * Required
            
        modification_date
            * DateTimeField
            * auto_now
            * The page's modification date
            * Required
            
        is_published
            * BooleanField
            * Is page published?
            * Default: False
            * Required
            
        content
            * TextField
            * The page's content
            * Required

    Managers::

        objects
            Default manager.
            Manager: models.Manager()

        published
            Only returns published pages.
            Manager: critica.apps.pages.managers.PublishedPageManager()
            
    Indexes::
    
        * author
        * slug
        * is_published

    """
    author = models.ForeignKey('auth.User', verbose_name=_('author'))
    title = models.CharField(_('title'), max_length=255)
    slug  = models.SlugField(_('slug'), max_length=255, unique=True, editable=False)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    is_published = models.BooleanField(_('published'), default=False, db_index=True)
    content = models.TextField(_('content'))
    
    objects = models.Manager()
    published = PublishedPageManager()
    
    class Meta:
        """ Model metadata. """
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        permissions = (
            ('can_publish_page', 'Can publish a page'),
        )

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.title

    def author_full_name(self):
        return self.author.get_full_name()
    author_full_name.short_description = _('author')

    @permalink
    def get_absolute_url(self):
        """ Returns page's absolute URL. """
        return ('pages_page', (), {
            'slug': self.slug,
        })

    def save(self):
        """ Object pre-saving operations. """
        self.slug = slugify(self.title)
        super(Page, self).save()


