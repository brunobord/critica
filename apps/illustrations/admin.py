# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.illustrations`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.illustrations.models import Illustration


class IllustrationAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Illustration`` model.
    
    """
    list_display = ('image_ld', 'category_ld', 'credits', 'legend', 'creation_date', 'modification_date')
    list_filter = ('category',)
    search_fields = ('image', 'credits', 'legend')
    ordering = ['legend', 'creation_date']
    date_hierarchy = 'creation_date'


basic_site.register(Illustration, IllustrationAdmin)
advanced_site.register(Illustration, IllustrationAdmin)

