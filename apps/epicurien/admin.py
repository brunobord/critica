# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.epicurien`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.epicurien.models import EpicurienArticleType, EpicurienArticle


class EpicurienArticleTypeAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``EpicurienArticleType`` model.
    
    """
    list_display = ('name', 'slug')
    
admin.site.register(EpicurienArticleType, EpicurienArticleTypeAdmin)
basic_site.register(EpicurienArticleType, EpicurienArticleTypeAdmin)
advanced_site.register(EpicurienArticleType, EpicurienArticleTypeAdmin)


class EpicurienArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``EpicurienArticle`` model.
    
    """
    list_display = ('title', 'type', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish', 'ald_illustration')
    list_filter = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'type')
    search_fields = ('title', 'summary', 'content')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'

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
            (_('Headline'), {'fields': ('author_nickname', 'title', 'opinion', 'publication_date')}),
            (_('Filling'), {'fields': ('issues', 'type', 'tags')}),
            (_('Illustration'), {'fields': ('illustration', 'use_default_illustration')}),
            (_('Content'), {'fields': ('summary', 'content')}),
            (_('Publication'), {'fields': publication_fields})
        ]
        return fieldsets

admin.site.register(EpicurienArticle, EpicurienArticleAdmin)
basic_site.register(EpicurienArticle, EpicurienArticleAdmin)
advanced_site.register(EpicurienArticle, EpicurienArticleAdmin)

