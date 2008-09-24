# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.notes`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.notes.models import NoteType, Note
from critica.apps.articles.admin import BaseArticleAdmin


class NoteTypeAdmin(admin.ModelAdmin):
    """
    Administration interface for ``NoteType`` model.
    
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ['name']

basic_site.register(NoteType, NoteTypeAdmin)
advanced_site.register(NoteType, NoteTypeAdmin)


class BaseNoteAdmin(BaseArticleAdmin):
    """
    Administration interface for ``BaseNote`` abstract model.
    Inherits from ``critica.apps.articles.admin.BaseArticleAdmin``.
    
    """
    list_display = ('title', 'ald_issues', 'category', 'type', 'ald_publication_date', 'ald_opinion', 'is_featured', 'view_count', 'ald_author', 'ald_author_nickname', 'is_ready_to_publish')
    list_filter = ('author', 'is_ready_to_publish', 'is_reserved', 'is_featured', 'type', 'category')

    def get_fieldsets(self, request, obj=None):
        """ Hook for specifying fieldsets for the add form. """
        fieldsets = [
            (_('Headline'), 
                {'fields': ('author_nickname', 'title', 'type', 'opinion')}
            ),
            (_('Filling'),
                {'fields': ('issues', 'category', 'tags')}
            ),
            (_('Content'),
                {'fields': ('summary', 'content')}
            ),
        ]
            
        validation_fields = []
        
        if request.user.has_perm('notes.can_feature_note'):
            validation_fields.append('is_featured')
        if request.user.has_perm('notes.can_reserve_note'):
            validation_fields.append('is_reserved')
        if request.user.has_perm('notes.can_publish_note'):
            validation_fields.append('is_ready_to_publish')
            
        if request.user.has_perm('notes.can_reserve_note') \
            or request.user.has_perm('notes.can_feature_note') \
            or request.user.has_perm('notes.can_publish_note'):
            fieldsets += [(_('Publication'), {'fields': validation_fields})]

        return fieldsets
    

class NoteAdmin(BaseNoteAdmin):
    """
    Administration interface for ``Note`` model.
    
    """
    pass


basic_site.register(Note, NoteAdmin)
advanced_site.register(Note, NoteAdmin)

