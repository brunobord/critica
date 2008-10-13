# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.ads`` application.

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.ads.models import Customer
from critica.apps.ads.models import AdCampaign
from critica.apps.ads.models import AdFormat
from critica.apps.ads.models import AdType
from critica.apps.ads.models import AdPage
from critica.apps.ads.models import AdLocation
from critica.apps.ads.models import Ad
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarouselBanner
from critica.apps.ads.models import AdCarousel


class CustomerAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Customer, CustomerAdmin)
basic_site.register(Customer, CustomerAdmin)
advanced_site.register(Customer, CustomerAdmin)


class AdCampaignAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(AdCampaign, AdCampaignAdmin)
basic_site.register(AdCampaign, AdCampaignAdmin)
advanced_site.register(AdCampaign, AdCampaignAdmin)


class AdFormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'width', 'height')
    ordering = ['width']
    
admin.site.register(AdFormat, AdFormatAdmin)
basic_site.register(AdFormat, AdFormatAdmin)
advanced_site.register(AdFormat, AdFormatAdmin)


class AdTypeAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(AdType, AdTypeAdmin)
basic_site.register(AdType, AdTypeAdmin)
advanced_site.register(AdType, AdTypeAdmin)


class AdPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'type')
    list_display_links = ('id', 'name')
    ordering = ['id']
    
admin.site.register(AdPage, AdPageAdmin)
basic_site.register(AdPage, AdPageAdmin)
advanced_site.register(AdPage, AdPageAdmin)


class AdLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    ordering = ['position']
    
admin.site.register(AdLocation, AdLocationAdmin)
basic_site.register(AdLocation, AdLocationAdmin)
advanced_site.register(AdLocation, AdLocationAdmin)


class AdAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('page', 'format', 'location', 'price'),
        }),
    )
    list_display = ('format', 'page', 'location', 'price')
    list_filter = ('format', 'page', 'location', 'price')
    
    def __call__(self, request, url):
        self.request = request
        return super(AdAdmin, self).__call__(request, url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(AdAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'location': 
            my_choices = [('', '---------')]
            my_choices.extend(AdLocation.objects.order_by('position').values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field
    
admin.site.register(Ad, AdAdmin)
basic_site.register(Ad, AdAdmin)
advanced_site.register(Ad, AdAdmin)


class AdBannerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('customer', 'campaign', 'type'),
        }),
        (_('Banner'), {
            'fields': ('banner', 'ads', 'link', 'description'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('customer', 'campaign', 'type', 'starting_date', 'ending_date')
    list_filter = ('customer', 'campaign', 'type')
    filter_vertical = ['ads']
         
    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdBanner, AdBannerAdmin)
basic_site.register(AdBanner, AdBannerAdmin)
advanced_site.register(AdBanner, AdBannerAdmin)


class AdCarouselBannerAdmin(admin.ModelAdmin):
    list_display = ('banner', 'description', 'submitter')
    list_filter = ['submitter']
         
    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdCarouselBanner, AdCarouselBannerAdmin)
basic_site.register(AdCarouselBanner, AdCarouselBannerAdmin)
advanced_site.register(AdCarouselBanner, AdCarouselBannerAdmin)


class AdCarouselAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('customer', 'campaign', 'type'),
        }),
        (_('Carousel'), {
            'fields': ('xml', 'banners', 'ads'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('customer', 'campaign', 'type', 'starting_date', 'ending_date')
    list_filter = ('customer', 'campaign', 'type')
    filter_vertical = ['ads', 'banners']
         
    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdCarousel, AdCarouselAdmin)
basic_site.register(AdCarousel, AdCarouselAdmin)
advanced_site.register(AdCarousel, AdCarouselAdmin)
