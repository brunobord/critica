# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.notes`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.notes.models import NoteType, NoteTypePosition, Note
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


class NoteTypePositionAdmin(admin.ModelAdmin):
    """
    Administration interface for ``NoteTypePosition`` model.
    
    """
    list_display = ('issue', 'type', 'position')
    search_fields = ('issue', 'type', 'position')
    ordering = ['issue']

#basic_site.register(NoteTypePosition, NoteTypePositionAdmin)
#advanced_site.register(NoteTypePosition, NoteTypePositionAdmin)


class BaseNoteAdmin(BaseArticleAdmin):
    """
    Administration interface for ``BaseNote`` abstract model.
    Inherits from ``critica.apps.articles.admin.BaseArticleAdmin``.
    
    """
    fieldsets = (
        (_('Headline'), 
            {'fields': ('author_nickname', 'title', 'type', 'opinion', 'is_featured')}
        ),
        (_('Filling'),
            {'fields': ('issues', 'category', 'tags')}
        ),
        (_('Content'),
            {'fields': ('content',)}
        ),
        (_('Publication'),
            {'fields': ('publication_date', 'status')}
        ),
    )
    list_display = ('title', 'ald_issues', 'category', 'type', 'ald_publication_date', 'ald_opinion', 'is_featured', 'view_count', 'ald_author', 'ald_author_nickname', 'status')
    list_filter = ('author', 'status', 'is_featured', 'type', 'category')
    

class NoteAdmin(BaseNoteAdmin):
    """
    Administration interface for ``Note`` model.
    
    """
    pass


basic_site.register(Note, NoteAdmin)
advanced_site.register(Note, NoteAdmin)

