# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.voyages`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.voyages.models import VoyagesArticle


class VoyagesArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``VoyagesArticle`` model.
    
    """
    fieldsets = (
        (_('Headline'), {
            'fields': ('author_nickname', 'title', 'localization', 'widget', 'opinion', 'publication_date'),
        }),
        (_('Filling'), {
            'fields': ('issues', 'tags'),
        }),
        (_('Image'), {
            'fields': ('image', 'image_legend', 'image_credits'),
        }),
        (_('Content'), {
            'fields': ('summary', 'content'),
        }),
        (_('Publication'), {
            'fields': ('is_featured', 'is_reserved', 'is_ready_to_publish'),
        }),
    )
    list_display  = ('title', 'localization', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish', 'ald_image')
    list_filter   = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'localization')
    search_fields = ('title', 'summary', 'content', 'localization')
    

# Registers
# ------------------------------------------------------------------------------
admin.site.register(VoyagesArticle, VoyagesArticleAdmin)
custom_site.register(VoyagesArticle, VoyagesArticleAdmin)

