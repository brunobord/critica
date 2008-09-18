# -*- coding: utf-8 -*-
""" 
Administration interface options for ``cockatoo.apps.journal`` models. 

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag, TaggedItem
from critica.apps.journal.models import Category, NoteType
from critica.apps.journal.models import Reportage, Illustration
from critica.apps.journal.models import Article, Note
from critica.apps.journal.models import Issue


class CategoryAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Category`` model.
    
    """
    list_display = ('name', 'slug_ld', 'description', 'creation_date', 'modification_date', 'image_ld')
    search_fields = ('name', 'description')
    ordering = ['name']


class NoteTypeAdmin(admin.ModelAdmin):
    """
    Administration interface for ``NoteType`` model.
    
    """
    list_display = ('name', 'position_on_page')
    search_fields = ('name',)
    ordering = ['position_on_page']


class ReportageAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Reportage`` model.
    
    """
    list_display = ('video_name', 'video_link', 'creation_date', 'modification_date', 'is_published')
    search_fields = ('video_name',)
    ordering = ('-creation_date',)
    date_hierarchy = 'creation_date'
    

class IllustrationAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Illustration`` model.
    
    """
    list_display = ('image_ld', 'category_ld', 'credits', 'legend', 'creation_date', 'modification_date')
    list_filter = ('category',)
    search_fields = ('image', 'credits', 'legend')
    ordering = ['legend', 'creation_date']
    date_hierarchy = 'creation_date'


class BaseArticleAdmin(admin.ModelAdmin):
    """
    Administration interface for ``BaseArticle`` abstract model.
    
    """
    list_display = ('title', 'category', 'publication_date', 'is_featured', 'is_reserved', 'view_count', 'author_ld')
    list_filter = ('author', 'is_featured', 'is_reserved', 'category')
    search_fields = ('title', 'content')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    
    class Media:
        """
        Model metadata.
        
        """
        js = (
            settings.MEDIA_URL + 'common/js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'common/js/textarea.js',
        )
        
    def get_form(self, request, obj=None, **kwargs):
        """
        Returns a Form class for use in the admin add view. This is used by
        add_view and change_view.
        
        Excludes fields depending on user permissions.
        
        """
        exclude = []
        if not request.user.has_perm('users.can_reserve_article'):
            exclude.append('is_reserved')
        if not request.user.has_perm('users.can_feature_article'):
            exclude.append('is_featured')
        defaults = {'exclude': exclude}
        defaults.update(kwargs)
        return super(BaseArticleAdmin, self).get_form(request, obj, **defaults)


class ArticleAdmin(BaseArticleAdmin):
    """
    Administration interface for ``Article`` model.
    
    """
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
            {'fields': ('publication_date', 'is_reserved', 'is_published')}
        ),
    )
    list_display = ('title', 'category', 'publication_date', 'opinion', 'is_featured', 'is_reserved', 'view_count', 'author_ld', 'is_published')
    search_fields = ('title', 'summary', 'content')

    def get_form(self, request, obj=None, **kwargs):
        exclude = []
        if not request.user.has_perm('users.can_validate_illustration'):
            exclude.append('is_illustrated')
        defaults = {'exclude': exclude}
        defaults.update(kwargs)
        return super(ArticleAdmin, self).get_form(request, obj, **defaults)


class NoteAdmin(BaseArticleAdmin):
    """
    Administration interface for ``Note`` model.
    
    """
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
            {'fields': ('publication_date', 'is_reserved', 'is_published')}
        ),
    )
    list_display = ('title', 'category', 'type_ld', 'publication_date', 'opinion', 'is_featured', 'is_reserved', 'view_count', 'author_ld', 'is_published')
    list_filter = ('author', 'is_featured', 'is_reserved', 'is_published', 'category')


class IssueAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Issue`` model.
    
    """
    list_display = ('number', 'publication_date', 'is_complete', 'is_published')
    list_filter = ('is_complete', 'is_published')
    search_fields = ('number',)
    ordering = ('-publication_date',)
    date_hierarchy = 'publication_date'
    

# Registers
# ------------------------------------------------------------------------------
admin.site.unregister(Tag)
admin.site.unregister(TaggedItem)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NoteType, NoteTypeAdmin)
admin.site.register(Reportage, ReportageAdmin)
admin.site.register(Illustration, IllustrationAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Issue, IssueAdmin)

