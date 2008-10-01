# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.voyages`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.voyages.models import VoyagesArticle


class VoyagesArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``VoyagesArticle`` model.
    
    """
    list_display = ('title', 'localization', 'ald_issues', 'tags', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'view_count', 'is_featured', 'is_reserved', 'is_ready_to_publish', 'ald_illustration')
    list_filter = ('author', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'localization')
    search_fields = ('title', 'summary', 'content', 'localization')
    
    def get_fieldsets(self, request, obj=None):
        """ 
        Hook for specifying fieldsets for the add form. 
        
        """
        fieldsets = [
            (_('Headline'), {'fields': ('author_nickname', 'title', 'localization', 'opinion', 'publication_date')}),
            (_('Filling'), {'fields': ('issues', 'tags')}),
            (_('Illustration'), {'fields': ('illustration', 'use_default_illustration')}),
            (_('Content'), {'fields': ('summary', 'content')}),
        ]
            
        publication_fields = []
        
        if request.user.has_perm('voyages.can_feature_article'):
            publication_fields.append('is_featured')
        if request.user.has_perm('voyages.can_reserve_article'):
            publication_fields.append('is_reserved')
        if request.user.has_perm('voyages.can_publish_article'):
            publication_fields.append('is_ready_to_publish')
            
        if request.user.has_perm('voyages.can_reserve_article') \
            or request.user.has_perm('voyages.can_feature_article') \
            or request.user.has_perm('voyages.can_publish_article'):
            fieldsets += [(_('Publication'), {'fields': publication_fields})]

        return fieldsets

admin.site.register(VoyagesArticle, VoyagesArticleAdmin)
basic_site.register(VoyagesArticle, VoyagesArticleAdmin)
advanced_site.register(VoyagesArticle, VoyagesArticleAdmin)

