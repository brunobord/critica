# -*- coding: utf-8 -*-
"""
Administration interface options of ``critica.apps.pages`` models.

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    """ 
    Administration interface options of ``Page`` model. 
    
    """
    list_display = ('title', 'ald_slug', 'creation_date', 'modification_date', 'is_published', 'ald_author')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'author')
    ordering = ['title']
    exclude = ['author']
    
    class Media:
        js = (
            settings.MEDIA_URL + 'common/js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'common/js/textarea.js',
        )
        
    def ald_slug(self, obj):
        """ 
        Formatted slug for admin list_display option. 
        
        """
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        return 'http://www.%s/pages/<strong>%s</strong>/' % (site.domain, obj.slug)
    ald_slug.allow_tags = True
    ald_slug.short_description = _('URL')
    
    def ald_author(self, obj):
        """
        Formatted author for admin list_display option.
        
        """
        if obj.author.get_full_name():
            return obj.author.get_full_name()
        else:
            return obj.author
    ald_author.short_description = _('author')
    
    def get_fieldsets(self, request, obj=None):
        """ 
        Hook for specifying fieldsets for the add form. 
        
        """
        publication_fields = []
        if request.user.has_perm('users.is_editor'):
            publication_fields.append('is_published')
        fieldsets = [
            (None, {'fields': ['title', 'content']}),
            (_('Publication'), {'fields': publication_fields}),
        ]
        return fieldsets
        
    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        Auto-save author.
        
        """
        if change == False:
            obj.author = request.user
        obj.save()

admin.site.register(Page, PageAdmin)
basic_site.register(Page, PageAdmin)
advanced_site.register(Page, PageAdmin)

