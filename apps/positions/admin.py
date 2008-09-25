# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.positions`` models. 

"""
from django.contrib import admin
from critica.apps.positions.models import CategoryPosition, NoteTypePosition
from critica.apps.admin.sites import basic_site, advanced_site


class CategoryPositionAdmin(admin.ModelAdmin):
    pass
    
basic_site.register(CategoryPosition, CategoryPositionAdmin)
advanced_site.register(CategoryPosition, CategoryPositionAdmin)


class NoteTypePositionAdmin(admin.ModelAdmin):
    pass
    
basic_site.register(NoteTypePosition, NoteTypePositionAdmin)
advanced_site.register(NoteTypePosition, NoteTypePositionAdmin)
