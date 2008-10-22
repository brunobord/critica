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
from critica.apps.ads.forms import CustomAdDefaultBannerForm
from critica.apps.ads.forms import CustomAdBannerForm

# Commons 
# ------------------------------------------------------------------------------
class CustomerAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Customer, CustomerAdmin)
custom_site.register(Customer, CustomerAdmin)



class AdCampaignAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(AdCampaign, AdCampaignAdmin)
custom_site.register(AdCampaign, AdCampaignAdmin)



class AdFormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'width', 'height')
    ordering = ['width']
    
admin.site.register(AdFormat, AdFormatAdmin)
custom_site.register(AdFormat, AdFormatAdmin)



class AdTypeAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(AdType, AdTypeAdmin)
custom_site.register(AdType, AdTypeAdmin)



class AdPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'type')
    list_display_links = ('id', 'name')
    ordering = ['id']
    
admin.site.register(AdPage, AdPageAdmin)
custom_site.register(AdPage, AdPageAdmin)



class AdLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    ordering = ['position']
    
admin.site.register(AdLocation, AdLocationAdmin)
custom_site.register(AdLocation, AdLocationAdmin)



# Banners 
# ------------------------------------------------------------------------------
class AdBannerPositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page', 'format', 'location', 'price'),
        }),
    )
    list_display = ('format', 'page', 'location', 'price')
    list_filter = ('format', 'page', 'location', 'price')
    
    def __call__(self, request, url):
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
    
admin.site.register(AdBannerPosition, AdBannerPositionAdmin)
custom_site.register(AdBannerPosition, AdBannerPositionAdmin)



class AdDefaultBannerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Banner'), {
            'fields': ('banner', 'positions', 'link', 'description'),
        }),
    )
    list_display = ('banner', 'ald_positions')
    filter_vertical = ['positions']
    form = CustomAdDefaultBannerForm

    def ald_positions(self, obj):
        html = '<table class="banner-ads-info"><tbody>'
        for ad in obj.positions.all():
            html += '<tr><td style="border:none; width: 220px; font-variant: small-caps;">%s</td><td style="border:none;">%s</td></tr>' % (ad.page, ad.location)
        html += '</tbody></table>'
        return html
    ald_positions.allow_tags = True
    ald_positions.short_description = _('positions')
    
    def ald_banner(self, obj):
        for ad in obj.positions.all():
            if not ad.format:
                return None
            else:
                return ad.format
    ald_banner.allow_tags = True
    ald_banner.short_description = _('banner')
    
    def save_model(self, request, obj, form, change):
        form = self.form
        if change == False:
            obj.submitter = request.user
        obj.save()
        
admin.site.register(AdDefaultBanner, AdDefaultBannerAdmin)
custom_site.register(AdDefaultBanner, AdDefaultBannerAdmin)



class AdBannerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('campaign', 'type'),
        }),
        (_('Banner'), {
            'fields': ('banner', 'positions', 'link', 'description'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('campaign', 'type', 'ald_positions', 'starting_date', 'ending_date')
    list_filter = ('campaign', 'type')
    filter_vertical = ['positions']
    form = CustomAdBannerForm

    def ald_positions(self, obj):
        html = '<table class="banner-ads-info"><tbody>'
        for ad in obj.positions.all():
            html += '<tr><td style="border:none; width: 220px; font-variant: small-caps;">%s</td><td style="border:none;">%s</td></tr>' % (ad.page, ad.location)
        html += '</tbody></table>'
        return html
    ald_positions.allow_tags = True
    ald_positions.short_description = (_('positions'))
    
    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdBanner, AdBannerAdmin)
custom_site.register(AdBanner, AdBannerAdmin)



# Carousels
# ------------------------------------------------------------------------------
class AdCarouselPositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page', 'format', 'location', 'price'),
        }),
    )
    list_display = ('page', 'format', 'location', 'price')
    list_filter = ('format', 'page', 'location', 'price')
    
    def __call__(self, request, url):
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
    
admin.site.register(AdCarouselPosition, AdCarouselPositionAdmin)
custom_site.register(AdCarouselPosition, AdCarouselPositionAdmin)



class AdCarouselAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('campaign', 'type'),
        }),
        (_('Carousel'), {
            'fields': ('folder', 'positions'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('campaign', 'folder', 'type', 'starting_date', 'ending_date')
    list_filter = ('campaign', 'type')
    filter_vertical = ['positions']

    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdCarousel, AdCarouselAdmin)
custom_site.register(AdCarousel, AdCarouselAdmin)



