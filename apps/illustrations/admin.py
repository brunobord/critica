# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.illustrations`` models. 

"""
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.illustrations.models import Illustration, IllustrationOfTheDay


class IllustrationAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Illustration`` model.
    
    """
    list_display = ('ald_image', 'ald_category', 'credits', 'legend', 'creation_date', 'modification_date')
    list_filter = ('category',)
    search_fields = ('image', 'credits', 'legend')
    ordering = ['legend', 'creation_date']
    date_hierarchy = 'creation_date'

    def ald_image(self, obj):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, obj.image, obj.legend)
    ald_image.allow_tags = True
    ald_image.short_description = _('Illustration')

    def ald_category(self, obj):
        """
        Formatted category for admin list_display option.
        
        """
        return '<strong>%s</strong>' % obj.category
    ald_category.allow_tags = True
    ald_category.short_description = _('Category')

admin.site.register(Illustration, IllustrationAdmin)
basic_site.register(Illustration, IllustrationAdmin)
advanced_site.register(Illustration, IllustrationAdmin)


class IllustrationOfTheDayAdmin(admin.ModelAdmin):    
    """
    Administration interface for ``IllustrationOfTheDay`` model.
    
    """
    list_display = ('ald_image', 'credits', 'legend', 'creation_date', 'modification_date')
    search_fields = ('image', 'credits', 'legend')
    ordering = ['legend', 'creation_date']
    date_hierarchy = 'creation_date'

    def ald_image(self, obj):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, obj.image, obj.legend)
    ald_image.allow_tags = True
    ald_image.short_description = _('Illustration')

admin.site.register(IllustrationOfTheDay, IllustrationOfTheDayAdmin)
basic_site.register(IllustrationOfTheDay, IllustrationOfTheDayAdmin)
advanced_site.register(IllustrationOfTheDay, IllustrationOfTheDayAdmin)

