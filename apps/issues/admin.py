# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue


class IssueAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Issue`` model.
    
    """
    list_display = ('number', 'publication_date', 'status')
    list_filter = ('status',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    radio_fields = {'status': admin.VERTICAL}
    date_hierarchy = 'publication_date'

basic_site.register(Issue, IssueAdmin)
advanced_site.register(Issue, IssueAdmin)


