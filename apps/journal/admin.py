# -*- coding: utf-8 -*-
""" 
Administration interface options for ``cockatoo.apps.journal`` models. 

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag, TaggedItem
from critica.apps.journal.models import Category
from critica.apps.journal.models import Reportage, Illustration
from critica.apps.journal.models import Article, Note
from critica.apps.journal.models import Issue


# Category
# ------------------------------------------------------------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_slug', 'description', 'creation_date', 'modification_date', 'image_thumbnail',)
    search_fields = ('name', 'description')
    ordering = ['name']


# Reportage
# ------------------------------------------------------------------------------
class ReportageAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'video_link', 'creation_date', 'modification_date', 'is_published')
    search_fields = ('video_name',)
    ordering = ('-creation_date',)
    date_hierarchy = 'creation_date'
    

# Illustration
# ------------------------------------------------------------------------------
class IllustrationAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'bolded_category', 'credits', 'legend', 'creation_date', 'modification_date')
    list_filter = ('category',)
    search_fields = ('image', 'credits', 'legend')
    ordering = ['legend', 'creation_date']
    date_hierarchy = 'creation_date'


# Articles: article / note
# ------------------------------------------------------------------------------
class BaseArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publication_date', 'is_featured', 'is_reserved', 'view_count', 'author_full_name')
    list_filter = ('author', 'is_featured', 'is_reserved', 'category')
    search_fields = ('title', 'content')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    
    class Media:
        js = (
            settings.MEDIA_URL + 'common/js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'common/js/textarea.js',
        )
        
    def get_form(self, request, obj=None, **kwargs):
        exclude = []
        if not request.user.has_perm('users.can_reserve_article'):
            exclude.append('is_reserved')
        if not request.user.has_perm('users.can_feature_article'):
            exclude.append('is_featured')
        defaults = {'exclude': exclude}
        defaults.update(kwargs)
        return super(BaseArticleAdmin, self).get_form(request, obj, **defaults)


class ArticleAdmin(BaseArticleAdmin):
    fieldsets = (
        (_('Headline'), 
            {'fields': ('title', 'opinion', 'is_featured')}
        ),
        (_('Filling'),
            {'fields': ('issues', 'category', 'tags')},
        ),
        (_('Illustration'),
            {'fields': ('illustration', 'use_default_illustration')}
        ),
        (_('Content'),
            {'fields': ('summary', 'content')}
        ),
        (_('Publication'),
            {'fields': ('publication_date', 'status', 'is_reserved')}
        ),
    )
    list_display = ('title', 'category', 'publication_date', 'opinion', 'is_featured', 'is_reserved', 'view_count', 'author_full_name', 'status')
    search_fields = ('title', 'summary', 'content')

    def get_form(self, request, obj=None, **kwargs):
        exclude = []
        if not request.user.has_perm('users.can_validate_illustration'):
            exclude.append('is_illustrated')
        defaults = {'exclude': exclude}
        defaults.update(kwargs)
        return super(ArticleAdmin, self).get_form(request, obj, **defaults)


class NoteAdmin(BaseArticleAdmin):
    fieldsets = (
        (_('Headline'), 
            {'fields': ('title', 'type', 'opinion', 'is_featured')}
        ),
        (_('Filling'),
            {'fields': ('issues', 'category', 'tags')}
        ),
        (_('Content'),
            {'fields': ('content',)}
        ),
        (_('Publication'),
            {'fields': ('publication_date', 'status', 'is_reserved')}
        ),
    )
    list_display = ('title', 'category', 'bolded_type', 'publication_date', 'opinion', 'is_featured', 'is_reserved', 'view_count', 'author_full_name', 'status')
    list_filter = ('author', 'is_featured', 'is_reserved', 'status', 'category')


# Issues
# ------------------------------------------------------------------------------
class IssueAdmin(admin.ModelAdmin):    
    list_display = ('number', 'publication_date', 'is_complete')
    list_filter = ('is_complete',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    date_hierarchy = 'publication_date'
    

# Registers
# ------------------------------------------------------------------------------
admin.site.unregister(Tag)
admin.site.unregister(TaggedItem)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reportage, ReportageAdmin)
admin.site.register(Illustration, IllustrationAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Issue, IssueAdmin)

