# -*- coding: utf-8 -*-
"""
Administration interface options for ``cockatoo.apps.pages`` models.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Page`` model. """
    list_display = ('title', 'slug', 'creation_date', 'modification_date', 'author', 'is_published')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'author')
    ordering = ('title',)

admin.site.register(Page, PageAdmin)
