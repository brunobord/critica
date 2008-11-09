# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.ads`` application.

"""
import os
from django.conf import settings
from django.db import models
from django.db.models import permalink
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from critica.apps.ads import settings as ads_settings


# Customer / Campaign
# ------------------------------------------------------------------------------
class Customer(models.Model):
    """
    Customer.
    
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter the customer name.'), unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % (self.name)


class AdCampaign(models.Model):
    """
    Ad campaign.
    
    """
    customer = models.ForeignKey('ads.Customer', verbose_name=_('customer'), help_text=_('Please, select or add a customer.'))
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter the campaign name.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad campaign')
        verbose_name_plural = _('ad campaigns')
        unique_together = (('customer', 'name'),)
    
    @permalink
    def get_preview_url(self):
        """ 
        Returns ads preview URL.
        
        """
        return ('ads_preview_home', (), {
            'campaign_id': self.id,
        })
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s' % (self.customer, self.name)


# Commons
# ------------------------------------------------------------------------------
class AdFormat(models.Model):
    """
    Ad format.
    
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this format.'), unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    width = models.IntegerField(_('width'), help_text=_('Please, enter the format width.'))
    height = models.IntegerField(_('height'), help_text=_('Please, enter the format height.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad format')
        verbose_name_plural = _('ad formats')
        unique_together = (('width', 'height'),)
 
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s - %sx%s' % (self.name, self.width, self.height)
        
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.name)
        super(AdFormat, self).save()


class AdType(models.Model):
    """
    Ad type.
    
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this type.'), unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad type')
        verbose_name_plural = _('ad types')
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name


class AdPage(models.Model):
    """
    Ad page.
    
    """
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
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad page')
        verbose_name_plural = _('ad pages')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name

    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.name)
        super(AdPage, self).save()


class AdLocation(models.Model):
    """
    Ad location.
    
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('Please, enter a name for this location.'), unique=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    position = models.DecimalField(_('position'), max_digits=2, decimal_places=1, help_text=_('Please, enter a numerical position.'), unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad location')
        verbose_name_plural = _('ad locations')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name

    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.name)
        super(AdLocation, self).save()


# Banners (images / swf)
# ------------------------------------------------------------------------------
class AdBannerPosition(models.Model):
    """
    Ad banner position.
    
    """
    format = models.ForeignKey('ads.AdFormat', verbose_name=_('format'), help_text=_('Please, select the format of your banner.'))
    page = models.ForeignKey('ads.AdPage', verbose_name=_('page'), help_text=_('Please, select a page where to display the ad.'))
    location = models.ForeignKey('ads.AdLocation', verbose_name=_('location'), help_text=_('Please, select a location for this ad.'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Please, enter its price by month.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad banner position')
        verbose_name_plural = _('ad banner positions')
        unique_together = (('page', 'location'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s - %s -- %sx%s' % (self.page, self.location, self.format.width, self.format.height)


class AdDefaultBanner(models.Model):
    """
    Default ad banner.
    
    """
    banner = models.FileField(upload_to=ads_settings.DEFAULT_BANNER_UPLOAD_PATH, verbose_name=_('banner'), help_text=_('Please, select a banner to upload (image or swf).'))
    banner_extension  = models.CharField(_('banner extension'), max_length=5, blank=True, editable=False)
    banner_type = models.CharField(_('banner type'), max_length=15, blank=True, editable=False)
    format = models.ForeignKey('ads.AdFormat', verbose_name=_('format'), help_text=_('Please, select the format of your banner.'))
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    positions = models.ManyToManyField('ads.AdBannerPosition', verbose_name=_('positions'), null=True, blank=True, help_text=_('Please, select one or several positions.'))
    description = models.TextField(_('description'), blank=True, help_text=_('You can enter a short description (optional).'))
    link = models.URLField(_('link'), verify_exists=False, blank=True, help_text=_('When people will click on this ad, they will be redirected to this link (optional).'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('default ad banner')
        verbose_name_plural = _('default ad banners')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % (self.banner)

    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        # Saving extension
        import os.path
        s, ext = os.path.splitext(self.banner.name)
        self.banner_extension = ext[1:].lower()
        # Saving type (image or swf)
        image_extensions = ['jpeg', 'jpg', 'gif', 'png']
        if self.banner_extension in image_extensions:
            self.banner_type = 'image'
        elif self.banner_extension == 'swf':
            self.banner_type = 'swf'
        else:
            self.banner_type = 'unknown'
        super(AdDefaultBanner, self).save()


class AdBanner(models.Model):
    """
    Ad banner.
    
    """
    banner = models.FileField(upload_to=ads_settings.BANNER_UPLOAD_PATH, max_length=200, verbose_name=_('banner'), help_text=_('Please, select a banner to upload (image or swf).'))
    banner_extension  = models.CharField(_('banner extension'), max_length=5, blank=True, editable=False)
    banner_type = models.CharField(_('banner type'), max_length=15, blank=True, editable=False)
    format = models.ForeignKey('ads.AdFormat', verbose_name=_('format'), help_text=_('Please, select the format of your banner.'))
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    campaign = models.ForeignKey('ads.AdCampaign', verbose_name=_('campaign'), help_text=_('Please, select a campaign.'))
    type = models.ForeignKey('ads.AdType', verbose_name=_('type'), help_text=_('Please, select a ad type.'))
    positions = models.ManyToManyField('ads.AdBannerPosition', verbose_name=_('positions'), null=True, blank=True, help_text=_('Please, select one or several positions.'))
    description = models.TextField(_('description'), blank=True, help_text=_('You can enter a short description (optional).'))
    link = models.URLField(_('link'), verify_exists=False, blank=True, help_text=_('When people will click on this ad, they will be redirected to this link (optional).'))
    starting_date = models.DateField(_('starting date'), blank=True, null=True)
    ending_date = models.DateField(_('ending date'), blank=True, null=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('banner')
        verbose_name_plural = _('banners')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % (self.banner)
        
    def count_days(self):
        """
        Returns the number of days based on starting_date / ending_date fields.
        
        """
        import datetime
        dates = []
        for day in xrange((self.ending_date - self.starting_date).days + 1):
            dates.append(self.starting_date + datetime.timedelta(day))
        return len(dates)

    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        # Saving extension
        import os.path
        s, ext = os.path.splitext(self.banner.name)
        self.banner_extension = ext[1:].lower()
        # Saving type (image or swf)
        image_extensions = ['jpeg', 'jpg', 'gif', 'png']
        if self.banner_extension in image_extensions:
            self.banner_type = 'image'
        elif self.banner_extension == 'swf':
            self.banner_type = 'swf'
        else:
            self.banner_type = 'unknown'
        super(AdBanner, self).save()
    

# Carousels
# ------------------------------------------------------------------------------
class AdCarouselPosition(models.Model):
    """
    Ad carousel position.
    
    """
    format = models.ForeignKey('ads.AdFormat', verbose_name=_('format'), help_text=_('Please, select a format.'))
    page = models.ForeignKey('ads.AdPage', verbose_name=_('page'), help_text=_('Please, select a page where to display the ad.'))
    location = models.ForeignKey('ads.AdLocation', verbose_name=_('location'), help_text=_('Please, select a location for this ad.'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Please, enter its price by month.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad carousel position')
        verbose_name_plural = _('ad carousel positions')
        unique_together = (('page', 'location'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s - %s' % (self.page, self.location)


class AdCarousel(models.Model):
    """
    Ad carousel.
    
    """
    name = models.CharField(_('name'), max_length=255, unique=True, help_text=_('Please, enter a name for this carousel. It must be unique.'))
    slug = models.SlugField(_('slug'), max_length=255)
    campaign = models.ForeignKey('ads.AdCampaign', verbose_name=_('campaign'), help_text=_('Please, select a campaign.'))
    type = models.ForeignKey('ads.AdType', verbose_name=_('type'), help_text=_('Please, select a ad type.'))
    format = models.ForeignKey('ads.AdFormat', verbose_name=_('format'), help_text=_('Please, select a format.'))
    positions = models.ManyToManyField('ads.AdCarouselPosition', verbose_name=_('positions'), null=True, blank=True, help_text=_('Please, select one or several positions.'))
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    starting_date = models.DateField(_('starting date'), null=True, blank=True, db_index=True)
    ending_date = models.DateField(_('ending date'), null=True, blank=True, db_index=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('ad carousel')
        verbose_name_plural = _('ad carousels')

    def count_days(self):
        """
        Returns the number of days based on starting_date / ending_date fields.
        
        """
        import datetime
        dates = []
        for day in xrange((self.ending_date - self.starting_date).days + 1):
            dates.append(self.starting_date + datetime.timedelta(day))
        return len(dates)
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s (%s)' % (self.name, self.campaign)

    def get_xml_url(self):
        """
        Returns XML file URL.
        
        """
        return settings.MEDIA_URL + 'upload/ads/carousels/%s/carousel.xml' % self.slug
        
    def _generate_xml(self):
        """
        Generates Carousel XML file.
        
        """
        xml_file_path = settings.MEDIA_ROOT + 'upload/ads/carousels/%s/carousel.xml' % self.slug
        if os.path.exists(xml_file_path):
            os.remove(xml_file_path)
        xml_file = open(xml_file_path, 'w')
        xml_header = '''<?xml version="1.0" encoding="utf-8"?>
        
        <!--
        	fhShow Carousel 1.5 configuration file
        	Please visit http://www.critica.fr/ for more info
        -->
        
        <slide_show>
        	<options>
        		<background>#FFFFFF</background>		<!-- #RRGGBB, transparent -->
        		<interaction>
        			<speed>60</speed>
        			<!-- [-360,360] degrees per second -->
        			<default_speed>25</default_speed>
        			<!-- [-360,360] degrees per second -->
        			<default_view_point>80%</default_view_point>
        			<!-- [0,100] percentage -->
        			<reset_delay>5</reset_delay>
        			<!-- [0,600] seconds, 0 means never reset -->
        		</interaction>
                <!-- [0,600] seconds, 0 means never reset -->
        	</options>
        '''
        xml_header.strip()
        xml_file.write(xml_header)
        banners = AdCarouselBanner.objects.filter(carousel=self)
        for banner in banners:
            xml_file.write('<photo href="%s" target="_self">%s</photo>' % (banner.link, banner.banner.url) + "\n")
        xml_file.write('</slide_show>')
        xml_file.close()
    
    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        # Generates slug
        self.slug = slugify(self.name)
        # Generates XML file
        self._generate_xml()
        # Save
        super(AdCarousel, self).save()


def get_carousel_image_path(instance, filename):
    """
    Returns the path to upload carousel images.
    
    """
    return 'upload/ads/carousels/%s/images/%s' % (instance.carousel.slug, filename)
    

class AdCarouselBanner(models.Model):
    """
    Ad carousel banner
    
    """
    link = models.CharField(_('link'), max_length=255, help_text=_('Please, enter the banner link (URL).'))
    carousel = models.ForeignKey('ads.AdCarousel', verbose_name=_('carousel'), help_text=_('Please, select a carousel that will include this image.'))
    banner = models.ImageField(upload_to=get_carousel_image_path, verbose_name=_('banner'), help_text=_('Please, select a banner to upload.'))
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('carousel banner')
        verbose_name_plural = _('carousel banners')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s -- %s' % (self.carousel, self.link)


