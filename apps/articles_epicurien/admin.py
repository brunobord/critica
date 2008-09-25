# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.articles_epicurien`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.articles_epicurien.models import ArticleEpicurien, ArticleEpicurienType


class ArticleEpicurienTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    
admin.site.register(ArticleEpicurienType, ArticleEpicurienTypeAdmin)
basic_site.register(ArticleEpicurienType, ArticleEpicurienTypeAdmin)
advanced_site.register(ArticleEpicurienType, ArticleEpicurienTypeAdmin)


class ArticleEpicurienAdmin(BaseArticleAdmin):
    """
    Administration interface for ``Article`` model.
    
    """
    list_display = ('title', 'category', 'type', 'ald_issues', 'tags', 'ald_publication_date', 'ald_opinion', 'is_featured', 'ald_author', 'ald_author_nickname', 'view_count', 'is_ready_to_publish')
    list_filter = ('author', 'type', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    
    def get_fieldsets(self, request, obj=None):
        """ Hook for specifying fieldsets for the add form. """
        fieldsets = [
            (_('Headline'), 
                {'fields': ('author_nickname', 'title', 'opinion')}
            ),
            (_('Filling'),
                {'fields': ('issues', 'type', 'tags')},
            ),
            (_('Illustration'),
                {'fields': ('illustration', 'use_default_illustration')}
            ),
            (_('Content'),
                {'fields': ('summary', 'content')}
            ),
        ]
            
        validation_fields = []
        
        if request.user.has_perm('articles.can_feature_article'):
            validation_fields.append('is_featured')
        if request.user.has_perm('articles.can_reserve_article'):
            validation_fields.append('is_reserved')
        if request.user.has_perm('articles.can_publish_article'):
            validation_fields.append('is_ready_to_publish')
            
        if request.user.has_perm('articles.can_reserve_article') \
            or request.user.has_perm('articles.can_feature_article') \
            or request.user.has_perm('articles.can_publish_article'):
            fieldsets += [(_('Publication'), {'fields': validation_fields})]

        return fieldsets

admin.site.register(ArticleEpicurien, ArticleEpicurienAdmin)
basic_site.register(ArticleEpicurien, ArticleEpicurienAdmin)
advanced_site.register(ArticleEpicurien, ArticleEpicurienAdmin)

