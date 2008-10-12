# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.ads`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.ads import settings as ads_settings


class Customer(models.Model):
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter the customer name.'), unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        
    def __unicode__(self):
        return u'%s' % (self.name)


class AdCampaign(models.Model):
    customer = models.ForeignKey('ads.Customer', verbose_name=_('customer'), help_text=_('Please, select or add a customer.'))
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter the campaign name.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        unique_together = (('customer', 'name'),)
        
    def __unicode__(self):
        return u'%s -- %s' % (self.customer, self.name)


class AdFormat(models.Model):
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this format.'), unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    width = models.IntegerField(_('width'), help_text=_('Please, enter the format width.'))
    height = models.IntegerField(_('height'), help_text=_('Please, enter the format height.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        verbose_name = _('format')
        verbose_name_plural = _('formats')
        unique_together = (('width', 'height'),)
        
    def __unicode__(self):
        return u'%s - %sx%s' % (self.name, self.width, self.height)
        
    def save(self):
        self.slug = slugify(self.name)
        super(AdFormat, self).save()


class AdType(models.Model):
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this type.'), unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()

    class Meta:
        verbose_name = _('type')
        verbose_name_plural = _('types')
        
    def __unicode__(self):
        return u'%s' % self.name

    
class AdPage(models.Model):
    PAGE_TYPE_HOME = 1
    PAGE_TYPE_CATEGORY = 2
    PAGE_TYPE_CHOICES = (
        (PAGE_TYPE_HOME, _('Home')),
        (PAGE_TYPE_CATEGORY, _('Category')),
    )
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this page.'), unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    type = models.IntegerField(_('type'), choices=PAGE_TYPE_CHOICES, default=PAGE_TYPE_CATEGORY, help_text=_('Select the page type. Is the homepage? Is a category page?'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'), null=True, blank=True, help_text=_('If this page belongs to a category, please select this category.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)

    objects = models.Manager()

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        
    def __unicode__(self):
        return u'%s' % self.name
        
    def save(self):
        self.slug = slugify(self.name)
        super(AdPage, self).save()

      
class AdLocation(models.Model):
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this location.'), unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    position = models.DecimalField(_('position'), max_digits=2, decimal_places=1, help_text=_('Please, enter a numerical position.'), unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        
    def __unicode__(self):
        return u'%s' % self.name
        
    def save(self):
        self.slug = slugify(self.name)
        super(AdLocation, self).save()


AD_PERIOD_DAY = 1
AD_PERIOD_WEEK = 2
AD_PERIOD_MONTH = 3
AD_PERIOD_TRIMESTER = 4
AD_PERIOD_YEAR = 5
AD_PERIOD_CHOICES = (
    (AD_PERIOD_DAY, _('By day')),
    (AD_PERIOD_WEEK, _('By week')),
    (AD_PERIOD_MONTH, _('By month')),
    (AD_PERIOD_TRIMESTER, _('By trimester')),
    (AD_PERIOD_YEAR, _('By year')),
)
class Ad(models.Model):    
    banner = models.ImageField(upload_to=ads_settings.IMAGE_UPLOAD_PATH, max_length=200, verbose_name=_('banner'), help_text=_('Please, select a banner to upload.'))
    format = models.ForeignKey('ads.AdFormat', verbose_name=_('format'), help_text=_('Please, select the format of your banner.'))
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    customer = models.ForeignKey('ads.Customer', verbose_name=_('customer'), help_text=_('Please, select a customer.'))
    campaign = models.ForeignKey('ads.AdCampaign', verbose_name=_('campaign'), help_text=_('Please, select a campaign.'))
    starting_date = models.DateField(_('starting date'))
    ending_date = models.DateField(_('ending date'))
    type = models.ForeignKey('ads.AdType', verbose_name=_('type'), help_text=_('Please, select a ad type.'))
    page = models.ForeignKey('ads.AdPage', verbose_name=_('page'), help_text=_('Please, select a page where to display the ad.'))
    location = models.ForeignKey('ads.ADLocation', verbose_name=_('location'), help_text=_('Please, select a location for this ad.'))
    description = models.TextField(_('description'), blank=True, help_text=_('You can enter a short description (optional).'))
    link = models.URLField(_('link'), blank=True, help_text=_('When people will click on this ad, they will be redirected to this link (optional).'))
    offer_period_type = models.IntegerField(_('offer period type'), choices=AD_PERIOD_CHOICES, null=True, blank=True, help_text=_('If offer is period-based, please select a period type.'))
    offer_period_during = models.IntegerField(_('offer period during'), null=True, blank=True, help_text=_('If offer is period-based, please enter its during.'))
    price_global = models.DecimalField(_('global price'), max_digits=10, decimal_places=2, null=True, blank=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()

    class Meta:
        verbose_name = _('ad')
        verbose_name_plural = _('ads')
        unique_together = (('page', 'location'),)
        
    def __unicode__(self):
        return u'%s - %s - %s' % (self.customer, self.page, self.location)

