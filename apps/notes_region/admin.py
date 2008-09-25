# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.notes_region`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.notes_region.models import NoteRegion, NoteTypeRegion, NoteRegionFeatured
from critica.apps.notes.admin import BaseNoteAdmin


class NoteTypeRegionAdmin(admin.ModelAdmin):
    """
    Administration interface for ``NoteTypeRegion`` model.
    
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ['name']

admin.site.register(NoteTypeRegion, NoteTypeRegionAdmin)
basic_site.register(NoteTypeRegion, NoteTypeRegionAdmin)
advanced_site.register(NoteTypeRegion, NoteTypeRegionAdmin)


class NoteRegionFeaturedAdmin(admin.ModelAdmin):
    """
    Administration interface for ``NoteRegionFeatured`` model.
    
    """
    list_display = ('issue', 'type')
    search_fields = ('issue', 'type')
    ordering = ['issue']

admin.site.register(NoteRegionFeatured, NoteRegionFeaturedAdmin)
basic_site.register(NoteRegionFeatured, NoteRegionFeaturedAdmin)
advanced_site.register(NoteRegionFeatured, NoteRegionFeaturedAdmin)


class NoteRegionAdmin(BaseNoteAdmin):
    """
    Administration interface for ``NoteRegion`` model.
    Inherits from ``critica.apps.notes.admin.BaseNoteAdmin``.
    
    """
    pass

admin.site.register(NoteRegion, NoteRegionAdmin)
basic_site.register(NoteRegion, NoteRegionAdmin)
advanced_site.register(NoteRegion, NoteRegionAdmin)

