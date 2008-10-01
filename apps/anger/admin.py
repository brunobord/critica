# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.anger`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.anger.models import AngerArticle


class AngerArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``AngerArticle`` model.
    
    """
    list_display = ('title', 'ald_issues', 'tags', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'view_count', 'is_featured', 'is_reserved', 'is_ready_to_publish')
    list_filter = ('author', 'is_ready_to_publish', 'is_reserved', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    ordering = ['-publication_date']
    
    def get_fieldsets(self, request, obj=None):
        """ 
        Hook for specifying fieldsets for the add form. 
        
        """
        fieldsets = [
            (_('Headline'), {'fields': ('author_nickname', 'title')}),
            (_('Filling'), {'fields': ('issues', 'tags')}),
            (_('Content'), {'fields': ('summary', 'content')}),
        ]
            
        publication_fields = []
        
        if request.user.has_perm('anger.can_feature_article'):
            publication_fields.append('is_featured')
        if request.user.has_perm('anger.can_reserve_article'):
            publication_fields.append('is_reserved')
        if request.user.has_perm('anger.can_publish_article'):
            publication_fields.append('is_ready_to_publish')
            
        if request.user.has_perm('anger.can_reserve_article') \
            or request.user.has_perm('anger.can_feature_article') \
            or request.user.has_perm('anger.can_publish_article'):
            fieldsets += [(_('Publication'), {'fields': publication_fields})]

        return fieldsets

admin.site.register(AngerArticle, AngerArticleAdmin)
basic_site.register(AngerArticle, AngerArticleAdmin)
advanced_site.register(AngerArticle, AngerArticleAdmin)

