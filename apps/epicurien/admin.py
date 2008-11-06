# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.epicurien`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.epicurien.models import EpicurienArticleType
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.epicurien.forms import EpicurienArticleAdminModelForm


class EpicurienArticleTypeAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``EpicurienArticleType`` model.
    
    """
    list_display = ('name', 'slug')
    

class EpicurienArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``EpicurienArticle`` model.
    
    """
    fieldsets = (
        (_('Headline'), {
            'fields': ('author_nickname', 'title', 'opinion', 'publication_date'),
        }),
        (_('Filling'), {
            'fields': ('issues', 'type', 'tags'),
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
    list_display = ('title', 'type', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish', 'ald_image')
    list_filter = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'type')
    search_fields = ('title', 'summary', 'content')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    form = EpicurienArticleAdminModelForm


# Registers
# ------------------------------------------------------------------------------
admin.site.register(EpicurienArticleType, EpicurienArticleTypeAdmin)
custom_site.register(EpicurienArticleType, EpicurienArticleTypeAdmin)

admin.site.register(EpicurienArticle, EpicurienArticleAdmin)
custom_site.register(EpicurienArticle, EpicurienArticleAdmin)



