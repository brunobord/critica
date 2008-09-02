# -*- coding: utf-8 -*-
"""
Administration interface options for ``cockatoo.apps.pages`` models.

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    """ Administration interface options for ``Page`` model. """
    list_display = ('author', 'title', 'creation_date', 'modification_date', 'is_published', 'content')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'author')
    ordering = ('title',)
    
    class Media:
        js = (
            settings.MEDIA_URL + 'js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'js/textarea.js',
        )
        
    def get_fieldsets(self, request, obj=None):
        """ Hook for specifying fieldsets for the add form. """
        fieldsets = [
            (None, {'fields': ['author', 'title', 'content']}),
        ]
        
        if request.user.has_perm('users.can_publish_page'):
            fieldsets.append((_('Validation'), {'fields': ['is_published']}))
        
        return fieldsets


admin.site.register(Page, PageAdmin)

