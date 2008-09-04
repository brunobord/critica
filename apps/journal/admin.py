# -*- coding: utf-8 -*-
""" 
Administration interface options for ``cockatoo.apps.journal`` models. 

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag, TaggedItem
from critica.apps.journal.models import Category
from critica.apps.journal.models import Position
from critica.apps.journal.models import Reportage
from critica.apps.journal.models import Illustration
from critica.apps.journal.models import Type
from critica.apps.journal.models import Article
from critica.apps.journal.models import Issue
from critica.apps.journal.models import Page


class CategoryAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Category`` model. """
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class PositionAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Position`` model. """
    list_display = ('position', 'description')
    search_fields = ('description',)
    ordering = ('position',)
    

class ReportageAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Reportage`` model. """
    fieldsets = (
        (_('Video'), {
            'fields': ('video_name', 'video_link')
        }),
        (_('Validation'), {
            'fields': ('is_published',)
        }),
    )
    
    list_display = ('video_name', 'video_link', 'creation_date', 'modification_date', 'is_published')
    search_fields = ('video_name',)
    ordering = ('-creation_date',)
    date_hierarchy = 'creation_date'
    

class IllustrationAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Illustration`` model. """
    list_display = ('image', 'credits', 'legend', 'is_generic')
    list_filter = ('is_generic',)
    search_fields = ('image', 'credits', 'legend')
    ordering = ('legend',)
    date_hierarchy = 'creation_date'


class TypeAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Type`` model. """
    pass
    

class ArticleAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Article`` model. """
    list_display = ('issue', 'category', 'title', 'type', 'publication_date', 'is_featured', 'is_published', 'is_illustrated', 'is_reserved', 'author')
    list_filter = ('author', 'type', 'is_featured', 'is_published', 'is_illustrated', 'category')
    search_fiels = ('title', 'summary', 'content', 'citation')
    ordering = ('-publication_date',)
    date_hierarchy = 'publication_date'
    
    class Media:
        js = (
            settings.MEDIA_URL + 'js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'js/textarea.js',
        )
    
    def get_fieldsets(self, request, obj=None):
        """ Hook for specifying fieldsets for the add form. """
        fieldsets = [
            (_('Article'), {'fields': ['author', 'issue', 'category', 'type', 'title', 'tags', 'publication_date', 'summary', 'content']}),
            (_('Citation'), {'fields': ['citation']}),
        ]
    
        if request.user.has_perm('users.can_illustrate_article'):
            fieldsets.append((_('Illustration'), {'fields': ['illustration']}))
            
        validation_fields = []
        
        if request.user.has_perm('users.can_reserve_article'):
            validation_fields.append('is_reserved')
        if request.user.has_perm('users.can_feature_article'):
            validation_fields.append('is_featured')
        if request.user.has_perm('users.can_illustrate_article'):
            validation_fields.append('is_illustrated')
        if request.user.has_perm('users.can_publish_article'):
            validation_fields.append('is_published')
            
        if request.user.has_perm('users.can_reserve_article') \
            or request.user.has_perm('users.can_feature_article') \
            or request.user.has_perm('users.can_illustrate_article') \
            or request.user.has_perm('users.can_publish_article'):
            fieldsets += [(_('Validation'), {'fields': validation_fields})]
            
        return fieldsets


class IssueAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Issue`` model. """
    fieldsets = (
        (_('Issue'), {
            'fields': ('number', 'publication_date')
        }),
        (_('Validation'), {
            'fields': ('is_complete',)
        }),
    )
    
    list_display = ('number', 'publication_date', 'is_complete')
    list_filter = ('is_complete',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    date_hierarchy = 'publication_date'


class PageAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Page`` model. """
    fieldsets = (
        (_('Page'), {
            'fields': ('category', 'articles')
        }),
        (_('Attach to this page'), {
            'fields': ('illustration_of_the_day', 'reportage'),
        }),
        (_('Validation'), {
            'fields': ('is_complete',),
        }),
    )

    list_display = ('category', 'is_complete')
    list_filter = ('is_complete',)


admin.site.unregister(Tag)
admin.site.unregister(TaggedItem)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Reportage, ReportageAdmin)
admin.site.register(Illustration, IllustrationAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Page, PageAdmin)

