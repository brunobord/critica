# -*- coding: utf-8 -*-
"""
Administration interface options of ``critica.apps.pages`` models.

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    """ 
    Administration interface options of ``Page`` model. 
    
    """
    fieldsets = (
        (None, {
            'fields': ('title', 'content'),
        }),
        (_('Publication'), {
            'fields': ('is_published',),
        }),
    )
    list_display  = ('title', 'ald_slug', 'creation_date', 'modification_date', 'is_published', 'ald_author')
    search_fields = ('title', 'content')
    list_filter   = ('is_published', 'author')
    ordering      = ['title']
    exclude       = ['author']

    def ald_slug(self, obj):
        """ 
        Formatted slug for admin list_display option. 
        
        """
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        url = 'http://%s/pages/%s/' % (site.domain, obj.slug)
        return '<a href="%s"><strong>%s</strong></a>' % (url, url)
    ald_slug.allow_tags = True
    ald_slug.short_description = _('Slug')

    def ald_author(self, obj):
        """
        Formatted author for admin list_display option.
        
        """
        if obj.author.get_full_name():
            return obj.author.get_full_name()
        else:
            return obj.author
    ald_author.short_description = _('author')

    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        
        """
        if change == False:
            obj.author = request.user
        obj.save()


# Registers
# ------------------------------------------------------------------------------
admin.site.register(Page, PageAdmin)
custom_site.register(Page, PageAdmin)

