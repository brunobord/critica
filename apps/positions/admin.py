# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.positions`` models. 

"""
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from critica.apps.categories.models import Category
from critica.apps.positions.models import CategoryPosition
from critica.apps.positions.models import NotePosition
from critica.apps.positions.models import DefaultCategoryPosition
from critica.apps.positions.models import DefaultNotePosition
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.positions.models import IssueNotePosition
from critica.apps.positions.forms import CustomIssueCategoryPositionForm
from critica.apps.positions.forms import CustomIssueNotePositionForm
from critica.apps.positions import settings as positions_settings
from critica.apps.custom_admin.sites import custom_site


# Positions
# ------------------------------------------------------------------------------
class CategoryPositionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``CategoryPosition`` model.
    
    """
    list_display = ('name', 'slug')
    

class NotePositionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``NotePosition`` model.
    
    """
    list_display = ('name', 'slug')
    

# Default positions
# ------------------------------------------------------------------------------
class DefaultCategoryPositionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``DefaultCategoryPosition`` model.
    
    """
    list_display = ('category', 'position')
    

class DefaultNotePositionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``DefaultNotePosition`` model.
    
    """
    list_display = ('category', 'type', 'position')
    list_filter  = ('category', 'type', 'position')
    
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


# Issue positions
# ------------------------------------------------------------------------------
class IssueCategoryPositionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``IssueCategoryPosition`` model.
    
    """
    list_display  = ('issue', 'category', 'position')
    list_filter   = ('issue', 'category', 'position')
    search_fields = ('issue__number', 'category__name', 'position')
    form          = CustomIssueCategoryPositionForm


class IssueNotePositionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``IssueNotePosition`` model.
    
    """
    list_display  = ('issue', 'ald_category', 'type', 'position')
    list_filter   = ('issue', 'category', 'type', 'position')
    search_fields = ('issue__number', 'category__name', 'type__name', 'position')
    form          = CustomIssueNotePositionForm

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
        
    def ald_category(self, obj):
        """
        Formatted category for admin list display.
        
        """
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        return '<a href="http://%s/preview/%s/%s/" target="_blank">%s</a>' % (site.domain, obj.issue.secret_key, obj.category.slug, obj.category.name)
    ald_category.short_description = _('category')
    ald_category.allow_tags = True


# Registers
# ------------------------------------------------------------------------------
admin.site.register(CategoryPosition, CategoryPositionAdmin)
custom_site.register(CategoryPosition, CategoryPositionAdmin)

admin.site.register(NotePosition, NotePositionAdmin)
custom_site.register(NotePosition, NotePositionAdmin)

admin.site.register(DefaultCategoryPosition, DefaultCategoryPositionAdmin)
custom_site.register(DefaultCategoryPosition, DefaultCategoryPositionAdmin)

admin.site.register(DefaultNotePosition, DefaultNotePositionAdmin)
custom_site.register(DefaultNotePosition, DefaultNotePositionAdmin)

admin.site.register(IssueCategoryPosition, IssueCategoryPositionAdmin)
custom_site.register(IssueCategoryPosition, IssueCategoryPositionAdmin)

admin.site.register(IssueNotePosition, IssueNotePositionAdmin)
custom_site.register(IssueNotePosition, IssueNotePositionAdmin)


