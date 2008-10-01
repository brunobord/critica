# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.positions`` models. 

"""
from django.contrib import admin
from critica.apps.positions.models import CategoryPosition, NoteTypePosition
from critica.apps.admin.sites import basic_site, advanced_site


class CategoryPositionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'category', 'position')
    list_filter = ('issue', 'category', 'position')
    search_fields = ('issue__number', 'category__name', 'position')
    
admin.site.register(CategoryPosition, CategoryPositionAdmin)
basic_site.register(CategoryPosition, CategoryPositionAdmin)
advanced_site.register(CategoryPosition, CategoryPositionAdmin)


class NoteTypePositionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'category', 'type', 'position')
    list_filter = ('issue', 'category', 'type', 'position')
    search_fields = ('issue', 'category', 'type', 'position')
    
admin.site.register(NoteTypePosition, NoteTypePositionAdmin)
basic_site.register(NoteTypePosition, NoteTypePositionAdmin)
advanced_site.register(NoteTypePosition, NoteTypePositionAdmin)
