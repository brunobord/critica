# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.notes_region`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.notes_region.models import NoteRegion, NoteTypeRegion
from critica.apps.notes.admin import BaseNoteAdmin


class NoteTypeRegionAdmin(admin.ModelAdmin):
    """
    Administration interface for ``NoteTypeRegion`` model.
    
    """
    list_display = ('name', 'is_featured')
    search_fields = ('name',)
    ordering = ['name']

basic_site.register(NoteTypeRegion, NoteTypeRegionAdmin)
advanced_site.register(NoteTypeRegion, NoteTypeRegionAdmin)


class NoteRegionAdmin(BaseNoteAdmin):
    """
    Administration interface for ``NoteRegion`` model.
    Inherits from ``critica.apps.notes.admin.BaseNoteAdmin``.
    
    """
    pass

basic_site.register(NoteRegion, NoteRegionAdmin)
advanced_site.register(NoteRegion, NoteRegionAdmin)

