# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue
from critica.apps.categories.models import CategoryPosition
from critica.apps.notes.models import NoteTypePosition
from critica.apps.notes_region.models import NoteRegionFeatured


class CategoryPositionInline(admin.TabularInline):
    """
    Category position inline for ``Issue`` model.
    
    """
    model = CategoryPosition
    max_num = 1


class NoteTypePositionInline(admin.TabularInline):
    """
    Note type position inline for ``Issue`` model.
    
    """
    model = NoteTypePosition
    max_num = 1
    

class NoteRegionFeaturedInline(admin.TabularInline):
    """
    Featured region note inline for ``Issue`` model.
    
    """
    model = NoteRegionFeatured
    max_num = 1


class IssueAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Issue`` model.
    
    """
    list_display = ('number', 'publication_date', 'status')
    list_filter = ('status',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    radio_fields = {'status': admin.VERTICAL}
    date_hierarchy = 'publication_date'
    inlines = [
        CategoryPositionInline,
        NoteTypePositionInline,
        NoteRegionFeaturedInline,
    ]

basic_site.register(Issue, IssueAdmin)
advanced_site.register(Issue, IssueAdmin)


