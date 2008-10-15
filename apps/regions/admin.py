# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.regions`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
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
custom_site.register(Region, RegionAdmin)


class FeaturedRegionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``FeaturedRegion`` model.
    
    """
    list_display = ('issue', 'region')
    search_fields = ('issue', 'region')
    ordering = ['-issue']

admin.site.register(FeaturedRegion, FeaturedRegionAdmin)
custom_site.register(FeaturedRegion, FeaturedRegionAdmin)


class RegionNoteAdmin(BaseNoteAdmin):
    """
    Administration interface options of ``RegionNote`` model.
    Inherits from ``critica.apps.notes.admin.BaseNoteAdmin``.
    
    """
    list_display = ('title', 'region', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish')
    list_filter = ('issues', 'author', 'region', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured')
    search_fields = ('title', 'content', 'issues__number')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    exclude = ['author']
    
    def __call__(self, request, url):
        self.request = request
        return super(RegionNoteAdmin, self).__call__(request, url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(RegionNoteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'region': 
            my_choices = [('', '---------')]
            my_choices.extend(Region.objects.order_by('name').values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field
        
    def get_fieldsets(self, request, obj=None):
        """ 
        Hook for specifying fieldsets for the add form. 
        
        """
        publication_fields = []
        publication_fields.append('is_featured')
        publication_fields.append('is_reserved')
        if request.user.has_perm('users.is_editor'):
            publication_fields.append('is_ready_to_publish')
        fieldsets = [
            (_('Headline'), {'fields': ('author_nickname', 'title', 'opinion', 'publication_date')}),
            (_('Filling'), {'fields': ('issues', 'region', 'tags')}),
            (_('Content'), {'fields': ('content',)}),
            (_('Publication'), {'fields': publication_fields}),
        ]
        return fieldsets

admin.site.register(RegionNote, RegionNoteAdmin)
custom_site.register(RegionNote, RegionNoteAdmin)

