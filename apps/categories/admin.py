# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.categories`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.categories.models import Category, CategoryPosition


class CategoryAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Category`` model.
    
    """
    list_display = ('name', 'ald_slug', 'description', 'creation_date', 'modification_date', 'ald_image')
    search_fields = ('name', 'description')
    ordering = ['name']
    
    def ald_slug(self, obj):
        """ 
        Formatted slug for admin list_display option. 
        
        """
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        return 'http://www.%s/<strong>%s</strong>/' % (site.domain, obj.slug)
    ald_slug.allow_tags = True
    ald_slug.short_description = _('Slug')
    
    def ald_image(self):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, obj.image, obj.image_legend)
    ald_image.allow_tags = True
    ald_image.short_description = _('Default illustration')

basic_site.register(Category, CategoryAdmin)
advanced_site.register(Category, CategoryAdmin)


class CategoryPositionAdmin(admin.ModelAdmin):
    """
    Administration interface for ``CategoryPosition`` model.
    
    """
    list_display = ('issue', 'category', 'position')
    search_fields = ('issue', 'category', 'position')
    ordering = ['issue']

#basic_site.register(CategoryPosition, CategoryPositionAdmin)
#advanced_site.register(CategoryPosition, CategoryPositionAdmin)

