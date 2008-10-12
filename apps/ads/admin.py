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
        (_('Customer'), {
            'fields': ('customer', 'campaign', 'type', 'price_global'),
        }),
        (_('Banner'), {
            'fields': ('banner', 'format', 'description', 'link'),
        }),
        (_('Location'), {
            'fields': ('page', 'location'),
        }),
        (_('Offer by period'), {
            'fields': ('offer_by_period', 'offer_period_type', 'offer_period_during'),
        }),
        (_('Offer by issue'), {
            'fields': ('offer_by_issue', 'offer_issue_number'),
        }),
    )
    list_display = ('customer', 'campaign', 'type', 'format', 'page', 'location', 'offer_by_period', 'offer_by_issue', 'ald_price_per_issue', 'ald_price_global')
    list_filter = ('customer', 'campaign', 'type', 'format', 'page', 'location', 'offer_by_period', 'offer_by_issue')
    
    def ald_price_per_issue(self, obj):
        return '%s euro' % obj.price_per_issue
    ald_price_per_issue.short_description = _('price per issue')

    def ald_price_global(self, obj):
        return '%s euro' % obj.price_global
    ald_price_global.short_description = _('price global')
    
    def save_model(self, request, obj, form, change):
        obj.submitter = request.user
        obj.save()
    
admin.site.register(Ad, AdAdmin)
basic_site.register(Ad, AdAdmin)
advanced_site.register(Ad, AdAdmin)

