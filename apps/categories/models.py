# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.categories`` application.

"""
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from critica.apps.categories import settings as categories_settings


class Category(models.Model):
    """
    Category.
    
    """
    name              = models.CharField(_('name'), max_length=255, help_text=_('As short as possible.'))
    slug              = models.SlugField(_('URL'), max_length=255, blank=True, unique=True, editable=False)
    description       = models.CharField(_('description'), max_length=255, blank=True, help_text=_('A short description of the category. It will not be displayed on the website.'))
    image             = models.ImageField(upload_to=categories_settings.IMAGE_UPLOAD_PATH, max_length=200, help_text=_('Please, upload an image for this category (it will be used as default category illustration).'))
    image_credits     = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    image_legend      = models.CharField(_('legend'), max_length=100, blank=True, help_text=_('100 characters max.'))
    creation_date     = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name    
    
    def get_absolute_url(self):
        """
        Returns object absolute URL.
        
        """
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        return u'%s/%s/' % (site.domain, self.slug)

    def get_rss_url(self):
        """
        Returns category RSS feed URL.
        
        """
        site = Site.objects.get_current()
        url = 'http://%s/rss/rubriques/%s' % (site.domain, self.slug)
        return url

    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.name)
        super(Category, self).save()


