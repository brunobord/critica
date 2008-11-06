# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.anger`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.anger.models import AngerArticle
from critica.apps.anger.forms import AngerArticleAdminModelForm


class AngerArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``AngerArticle`` model.
    
    """
    fieldsets = (
        (_('Headline'), {
            'fields': ('author_nickname', 'title', 'publication_date'),
        }),
        (_('Filling'), {
            'fields': ('issues', 'tags'),
        }),
        (_('Content'), {
            'fields': ('summary', 'content'),
        }),
        (_('Publication'), {
            'fields': ('is_featured', 'is_reserved', 'is_ready_to_publish'),
        }),
    )
    list_display = ('title', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish')
    list_filter = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    ordering = ['-publication_date']
    form = AngerArticleAdminModelForm


# Registers
# ------------------------------------------------------------------------------
admin.site.register(AngerArticle, AngerArticleAdmin)
custom_site.register(AngerArticle, AngerArticleAdmin)

