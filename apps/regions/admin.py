# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.regions`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.regions.models import RegionNote
from critica.apps.regions.models import Region
from critica.apps.regions.models import FeaturedRegion
from critica.apps.notes.admin import BaseNoteAdmin


class RegionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Region`` model.
    
    """
    list_display  = ('name', 'slug')
    search_fields = ('name',)
    ordering      = ['name']


class FeaturedRegionAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``FeaturedRegion`` model.
    
    """
    list_display  = ('issue', 'region')
    search_fields = ('issue', 'region')
    ordering      = ['-issue']


class RegionNoteAdmin(BaseNoteAdmin):
    """
    Administration interface options of ``RegionNote`` model.
    
    """
    fieldsets = (
        (_('Headline'), {
            'fields': ('author_nickname', 'title', 'opinion', 'publication_date'),
        }),
        (_('Filling'), {
            'fields': ('issues', 'region', 'tags'),
        }),
        (_('Content'), {
            'fields': ('content',),
        }),
        (_('Publication'), {
            'fields': ('is_featured', 'is_reserved', 'is_ready_to_publish'),
        }),
    )
    list_display   = ('title', 'region', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish')
    list_filter    = ('issues', 'author', 'region', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured')
    search_fields  = ('title', 'content', 'issues__number')
    ordering       = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    exclude        = ['author']
    
    def __call__(self, request, url):
        """
        Adds current request object and current URL to this class.
        
        """
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


# Registers
# ------------------------------------------------------------------------------
admin.site.register(Region, RegionAdmin)
custom_site.register(Region, RegionAdmin)

admin.site.register(FeaturedRegion, FeaturedRegionAdmin)
custom_site.register(FeaturedRegion, FeaturedRegionAdmin)

admin.site.register(RegionNote, RegionNoteAdmin)
custom_site.register(RegionNote, RegionNoteAdmin)

