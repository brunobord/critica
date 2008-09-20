# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.categories`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Category`` model.
    
    """
    list_display = ('name', 'admin_formatted_slug', 'description', 'creation_date', 'modification_date', 'admin_image_thumbnail')
    search_fields = ('name', 'description')
    ordering = ['name']

basic_site.register(Category, CategoryAdmin)
advanced_site.register(Category, CategoryAdmin)

