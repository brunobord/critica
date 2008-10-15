# -*- coding: utf-8 -*-
"""
Administration interface options of ``critica.apps.quotas`` models.

"""
from django.contrib import admin
from critica.apps.custom_admin.sites import custom_site
from critica.apps.quotas.models import DefaultCategoryQuota, CategoryQuota


class DefaultCategoryQuotaAdmin(admin.ModelAdmin):
    """ 
    Administration interface options of ``DefaultCategoryQuota`` model. 
    
    """
    list_display = ('category', 'quota')
    search_fields = ('category', 'quota')
    list_filter = ('category',)
    ordering = ['category']

admin.site.register(DefaultCategoryQuota, DefaultCategoryQuotaAdmin)
custom_site.register(DefaultCategoryQuota, DefaultCategoryQuotaAdmin)


class CategoryQuotaAdmin(admin.ModelAdmin):
    """ 
    Administration interface options of ``CategoryQuota`` model. 
    
    """
    list_display = ('issue', 'category', 'quota')
    search_fields = ('issue__number', 'category__name', 'quota')
    list_filter = ('issue', 'category')
    ordering = ['-issue']
    
admin.site.register(CategoryQuota, CategoryQuotaAdmin)
custom_site.register(CategoryQuota, CategoryQuotaAdmin)
