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
from critica.apps.ads.models import Ad
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdCarousel


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
custom_site.register(Ad, AdAdmin)


class AdBannerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('campaign', 'type'),
        }),
        (_('Banner'), {
            'fields': ('banner', 'ads', 'link', 'description'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('campaign', 'type', 'ald_ads', 'starting_date', 'ending_date')
    list_filter = ('campaign', 'type')
    filter_vertical = ['ads']

    def ald_ads(self, obj):
        html = '<table class="banner-ads-info"><tbody>'
        for ad in obj.ads.all():
            html += '<tr><td style="border:none; width: 220px; font-variant: small-caps;">%s</td><td style="border:none;">%s</td></tr>' % (ad.page, ad.location)
        html += '</tbody></table>'
        return html
    ald_ads.allow_tags = True
    ald_ads.short_description = (_('positions'))
    
    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdBanner, AdBannerAdmin)
custom_site.register(AdBanner, AdBannerAdmin)


class AdCarouselAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Customer'), {
            'fields': ('customer', 'campaign', 'type'),
        }),
        (_('Carousel'), {
            'fields': ('folder', 'ads'),
        }),
        (_('During'), {
            'fields': ('starting_date', 'ending_date'),
        }),
    )
    list_display = ('folder', 'customer', 'campaign', 'type', 'starting_date', 'ending_date')
    list_filter = ('customer', 'campaign', 'type')
    filter_vertical = ['ads']

    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(AdCarousel, AdCarouselAdmin)
custom_site.register(AdCarousel, AdCarouselAdmin)


