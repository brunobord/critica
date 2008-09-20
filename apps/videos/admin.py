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
    list_display = ('name', 'link', 'creation_date', 'modification_date', 'submitter', 'status')
    search_fields = ('name',)
    ordering = ('-creation_date',)
    radio_fields = {'status': admin.VERTICAL}
    date_hierarchy = 'creation_date'

basic_site.register(Video, VideoAdmin)
advanced_site.register(Video, VideoAdmin)

