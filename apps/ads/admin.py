# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.ads`` application.

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.ads.models import Customer
from critica.apps.ads.models import AdCampaign
from critica.apps.ads.models import AdFormat
from critica.apps.ads.models import AdType
from critica.apps.ads.models import AdPage
from critica.apps.ads.models import AdLocation
from critica.apps.ads.models import AdBannerPosition
from critica.apps.ads.models import AdDefaultBanner
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarouselPosition
from critica.apps.ads.models import AdCarousel
from critica.apps.ads.models import AdCarouselBanner
from critica.apps.ads.forms import CustomAdDefaultBannerForm
from critica.apps.ads.forms import CustomAdBannerForm
from critica.apps.ads.forms import AdCarouselAdminForm
from critica.apps.ads.forms import AdCarouselBannerAdminForm

    
# Commons 
# ------------------------------------------------------------------------------
class CustomerAdmin(admin.ModelAdmin):
    pass
    

class AdCampaignAdmin(admin.ModelAdmin):
    pass
    

class AdFormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'width', 'height')
    ordering     = ['width']
    

class AdTypeAdmin(admin.ModelAdmin):
    pass
    

class AdPageAdmin(admin.ModelAdmin):
    list_display       = ('id', 'name', 'slug', 'type')
    list_display_links = ('id', 'name')
    ordering           = ['id']


class AdLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    ordering     = ['position']


# Banners 
# ------------------------------------------------------------------------------
class AdBannerPositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page', 'format', 'location', 'price'),
        }),
    )
    list_display = ('format', 'page', 'location', 'price')
    list_filter  = ('format', 'page', 'location', 'price')
    
    def __call__(self, request, url):
        """
        Adds current request object and current URL to this class.
        
        """
        self.request = request
        return super(AdBannerPositionAdmin, self).__call__(request, url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(AdBannerPositionAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'location': 
            my_choices = [('', '---------')]
            my_choices.extend(AdLocation.objects.order_by('position').values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field
    

class AdDefaultBannerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Banner'), {
            'fields': ('banner', 'format', 'positions', 'link', 'description'),
        }),
    )
    list_display    = ('banner', 'ald_positions')
    filter_vertical = ['positions']
    form            = CustomAdDefaultBannerForm

    def ald_positions(self, obj):
        """
        Formatted positions list for admin list display.
        
        """
        html = '<table class="banner-ads-info"><tbody>'
        for ad in obj.positions.all():
            html += '<tr><td style="border:none; width: 220px; font-variant: small-caps;">%s</td><td style="border:none;">%s</td></tr>' % (ad.page, ad.location)
        html += '</tbody></table>'
        return html
    ald_positions.allow_tags = True
    ald_positions.short_description = _('positions')

    def ald_banner(self, obj):
        """
        Formatted banner format for admin list display.
        
        """
        for ad in obj.positions.all():
            if not ad.format:
                return None
            else:
                return ad.format
    ald_banner.allow_tags = True
    ald_banner.short_description = _('banner')
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        
        """
        form = self.form
        if change == False:
            obj.submitter = request.user
        obj.save()


class AdBannerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('campaign', 'type'),
        }),
        (_('Banner'), {
            'fields': ('banner', 'format', 'positions', 'link', 'description'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display    = ('campaign', 'type', 'ald_positions', 'starting_date', 'ending_date', 'ald_submitter')
    list_filter     = ('campaign', 'type')
    filter_vertical = ['positions']
    form            = CustomAdBannerForm

    def ald_submitter(self, obj):
        """
        Formatted submitter name for admin list display.
        
        """
        if obj.submitter.get_full_name():
            return obj.submitter.get_full_name()
        else:
            return obj.submitter
    ald_submitter.short_description = _('submitter')
    
    def ald_positions(self, obj):
        """
        Formatted positions list for admin list display.
        
        """
        html = '<table class="banner-ads-info"><tbody>'
        for ad in obj.positions.all():
            html += '<tr><td style="border:none; width: 220px; font-variant: small-caps;">%s</td><td style="border:none;">%s</td></tr>' % (ad.page, ad.location)
        html += '</tbody></table>'
        return html
    ald_positions.allow_tags = True
    ald_positions.short_description = (_('positions'))

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        
        """
        if change == False:
            obj.submitter = request.user
        obj.save()
        

# Carousels
# ------------------------------------------------------------------------------
class AdCarouselBannerInline(admin.StackedInline):
    """
    AdCarouselBanner inline.
    
    """
    model = AdCarouselBanner
    extra = 10
    max_num = 10
    form = AdCarouselBannerAdminForm
    

class AdCarouselLocationAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``AdCarouselLocation`` model.
    
    """
    pass
    
    
class AdCarouselPositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page', 'format', 'location', 'price'),
        }),
    )
    list_display = ('page', 'format', 'location', 'price')
    list_filter  = ('format', 'page', 'location', 'price')
    
    def __call__(self, request, url):
        """
        Adds current request object and current URL to this class.
        
        """
        self.request = request
        return super(AdCarouselPositionAdmin, self).__call__(request, url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(AdCarouselPositionAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'location': 
            my_choices = [('', '---------')]
            my_choices.extend(AdLocation.objects.order_by('position').values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field    


class AdCarouselAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('campaign', 'type'),
        }),
        (_('Carousel'), {
            'fields': ('name', 'format', 'positions'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('name', 'campaign', 'type', 'ald_positions', 'starting_date', 'ending_date', 'ald_submitter')
    list_filter = ('campaign', 'type')
    filter_vertical = ['positions']
    form = AdCarouselAdminForm
    inlines = [
        AdCarouselBannerInline,
    ]
    
    def ald_submitter(self, obj):
        """
        Formatted submitter name for admin list display.
        
        """
        if obj.submitter.get_full_name():
            return obj.submitter.get_full_name()
        else:
            return obj.submitter
    ald_submitter.short_description = _('submitter')
            
    def ald_positions(self, obj):
        """
        Formatted positions list for admin list display.
        
        """
        html = '<table class="banner-ads-info"><tbody>'
        for ad in obj.positions.all():
            html += '<tr><td style="border:none; width: 220px; font-variant: small-caps;">%s</td><td style="border:none;">%s</td></tr>' % (ad.page, ad.location)
        html += '</tbody></table>'
        return html
    ald_positions.allow_tags = True
    ald_positions.short_description = (_('positions'))

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(AdCarouselAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'format': 
            my_choices = [('', '---------')]
            my_choices.extend(AdFormat.objects.filter(slug__in=['carousel-450', 'carousel-320']).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field  

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        
        """
        if change == False:
            obj.submitter = request.user
        obj.save()


class AdCarouselBannerAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``AdCarouselBanner`` model.
    
    """
    pass


# Registers
# ------------------------------------------------------------------------------
admin.site.register(Customer, CustomerAdmin)
custom_site.register(Customer, CustomerAdmin)

admin.site.register(AdCampaign, AdCampaignAdmin)
custom_site.register(AdCampaign, AdCampaignAdmin)

admin.site.register(AdFormat, AdFormatAdmin)
custom_site.register(AdFormat, AdFormatAdmin)

admin.site.register(AdType, AdTypeAdmin)
custom_site.register(AdType, AdTypeAdmin)

admin.site.register(AdPage, AdPageAdmin)
custom_site.register(AdPage, AdPageAdmin)

admin.site.register(AdLocation, AdLocationAdmin)
custom_site.register(AdLocation, AdLocationAdmin)

admin.site.register(AdBannerPosition, AdBannerPositionAdmin)
custom_site.register(AdBannerPosition, AdBannerPositionAdmin)

admin.site.register(AdDefaultBanner, AdDefaultBannerAdmin)
custom_site.register(AdDefaultBanner, AdDefaultBannerAdmin)

admin.site.register(AdBanner, AdBannerAdmin)
custom_site.register(AdBanner, AdBannerAdmin)

admin.site.register(AdCarouselPosition, AdCarouselPositionAdmin)
custom_site.register(AdCarouselPosition, AdCarouselPositionAdmin)

admin.site.register(AdCarouselBanner, AdCarouselBannerAdmin)
custom_site.register(AdCarouselBanner, AdCarouselBannerAdmin)

admin.site.register(AdCarousel, AdCarouselAdmin)
custom_site.register(AdCarousel, AdCarouselAdmin)

