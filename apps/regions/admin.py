# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.regions`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.regions.models import RegionNote, Region, FeaturedRegion
from critica.apps.notes.admin import BaseNoteAdmin


class RegionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Region`` model.
    
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ['name']

admin.site.register(Region, RegionAdmin)
basic_site.register(Region, RegionAdmin)
advanced_site.register(Region, RegionAdmin)


class FeaturedRegionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``FeaturedRegion`` model.
    
    """
    list_display = ('issue', 'region')
    search_fields = ('issue', 'region')
    ordering = ['-issue']

admin.site.register(FeaturedRegion, FeaturedRegionAdmin)
basic_site.register(FeaturedRegion, FeaturedRegionAdmin)
advanced_site.register(FeaturedRegion, FeaturedRegionAdmin)


class RegionNoteAdmin(BaseNoteAdmin):
    """
    Administration interface options of ``RegionNote`` model.
    Inherits from ``critica.apps.notes.admin.BaseNoteAdmin``.
    
    """
    list_display = ('title', 'region', 'ald_issues', 'tags', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'view_count', 'is_featured', 'is_reserved', 'is_ready_to_publish')
    list_filter = ('author', 'region', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured')
    search_fields = ('title', 'content', 'issues__number')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    exclude = ['author']
    
    def get_fieldsets(self, request, obj=None):
        """ 
        Hook for specifying fieldsets for the add form. 
        
        """
        fieldsets = [
            (_('Headline'), {'fields': ('author_nickname', 'title', 'opinion', 'publication_date')}),
            (_('Filling'), {'fields': ('issues', 'region', 'tags')}),
            (_('Content'), {'fields': ('content',)}),
        ]
        
        publication_fields = []
        
        publication_fields.append('is_featured')
        
        if request.user.has_perm('userprofile.is_editor'):
            publication_fields.append('is_reserved')
            
        if request.user.has_perm('userprofile.is_editor'):
            publication_fields.append('is_ready_to_publish')
            
        if request.user.has_perm('userprofile.is_editor'):
            fieldsets += [(_('Publication'), {'fields': publication_fields})]
        
        return fieldsets

admin.site.register(RegionNote, RegionNoteAdmin)
basic_site.register(RegionNote, RegionNoteAdmin)
advanced_site.register(RegionNote, RegionNoteAdmin)

