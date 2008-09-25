# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue
from critica.apps.positions.models import CategoryPosition


class CategoryPositionInline(admin.TabularInline):
    """
    Category position inline for ``Issue`` model.
    
    """
    model = CategoryPosition
    max_num = 13
    
    
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
    inlines = [CategoryPositionInline]


admin.site.register(Issue, IssueAdmin)
basic_site.register(Issue, IssueAdmin)
advanced_site.register(Issue, IssueAdmin)


