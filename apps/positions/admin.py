# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.positions`` models. 

"""
from django.contrib import admin
from critica.apps.categories.models import Category
from critica.apps.positions.models import CategoryPosition, NotePosition
from critica.apps.positions.models import DefaultCategoryPosition, DefaultNotePosition
from critica.apps.positions.models import IssueCategoryPosition, IssueNotePosition
from critica.apps.positions import settings as positions_settings
from critica.apps.admin.sites import basic_site, advanced_site


# Positions
# ------------------------------------------------------------------------------
class CategoryPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    
admin.site.register(CategoryPosition, CategoryPositionAdmin)
basic_site.register(CategoryPosition, CategoryPositionAdmin)
advanced_site.register(CategoryPosition, CategoryPositionAdmin)

class NotePositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    
admin.site.register(NotePosition, NotePositionAdmin)
basic_site.register(NotePosition, NotePositionAdmin)
advanced_site.register(NotePosition, NotePositionAdmin)

# Default positions
# ------------------------------------------------------------------------------
class DefaultCategoryPositionAdmin(admin.ModelAdmin):
    list_display = ('category', 'position')
    
admin.site.register(DefaultCategoryPosition, DefaultCategoryPositionAdmin)
basic_site.register(DefaultCategoryPosition, DefaultCategoryPositionAdmin)
advanced_site.register(DefaultCategoryPosition, DefaultCategoryPositionAdmin)

class DefaultNotePositionAdmin(admin.ModelAdmin):
    list_display = ('category', 'type', 'position')
    list_filter = ('category', 'type', 'position')
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(DefaultNotePositionAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'category':
            my_choices = [('', '---------')]
            my_choices.extend(Category.objects.exclude(slug__in=positions_settings.EXCLUDED_CATEGORIES).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field
    
admin.site.register(DefaultNotePosition, DefaultNotePositionAdmin)
basic_site.register(DefaultNotePosition, DefaultNotePositionAdmin)
advanced_site.register(DefaultNotePosition, DefaultNotePositionAdmin)

# Issue positions
# ------------------------------------------------------------------------------
class IssueCategoryPositionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'category', 'position')
    list_filter = ('issue', 'category', 'position')
    search_fields = ('issue__number', 'category__name', 'position')
    
admin.site.register(IssueCategoryPosition, IssueCategoryPositionAdmin)
basic_site.register(IssueCategoryPosition, IssueCategoryPositionAdmin)
advanced_site.register(IssueCategoryPosition, IssueCategoryPositionAdmin)

class IssueNotePositionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'category', 'type', 'position')
    list_filter = ('issue', 'category', 'type', 'position')
    search_fields = ('issue__number', 'category__name', 'type__name', 'position')
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(IssueNotePositionAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'category':
            my_choices = [('', '---------')]
            my_choices.extend(Category.objects.exclude(slug__in=positions_settings.EXCLUDED_CATEGORIES).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field
    
admin.site.register(IssueNotePosition, IssueNotePositionAdmin)
basic_site.register(IssueNotePosition, IssueNotePositionAdmin)
advanced_site.register(IssueNotePosition, IssueNotePositionAdmin)

