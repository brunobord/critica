# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.videos`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.videos.models import Video


class VideoAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Video`` model.
    
    """
    list_display = ('name', 'link', 'creation_date', 'modification_date', 'submitter', 'is_reserved', 'is_ready_to_publish')
    search_fields = ('name',)
    ordering = ('-creation_date',)
    date_hierarchy = 'creation_date'

admin.site.register(Video, VideoAdmin)
basic_site.register(Video, VideoAdmin)
advanced_site.register(Video, VideoAdmin)

