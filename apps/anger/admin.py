# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.anger`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.anger.models import AngerArticle


class AngerArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``AngerArticle`` model.
    
    """
    list_display  = ('title', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish')
    list_filter   = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    ordering      = ['-publication_date']
    
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
            (_('Headline'), {'fields': ('author_nickname', 'title', 'publication_date')}),
            (_('Filling'), {'fields': ('issues', 'tags')}),
            (_('Content'), {'fields': ('summary', 'content')}),
            (_('Publication'), {'fields': publication_fields}),
        ]
        return fieldsets

admin.site.register(AngerArticle, AngerArticleAdmin)
custom_site.register(AngerArticle, AngerArticleAdmin)

