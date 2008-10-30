# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.polls`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from critica.apps.custom_admin.sites import custom_site
from critica.apps.polls.models import Poll
from critica.apps.polls.models import Choice
from critica.apps.polls.models import Vote


class ChoiceInline(admin.TabularInline):
    """ 
    Choice Tabular Inline used into Poll. 
    
    """
    model = Choice
    max_num = 8 



class PollAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Poll`` model.
    
    """
    fieldsets = (
        (None, {'fields': ('title', 'issues', 'tags', 'is_published')}),
    )
    list_display      = ('title', 'ald_issues', 'creation_date', 'modification_date', 'is_published', 'submitter')
    list_filter       = ('issues', 'is_published', 'submitter')
    filter_horizontal = ('issues',)
    search_fields     = ('title',)
    ordering          = ('-creation_date',)
    date_hierarchy    = 'creation_date'
    inlines           = [ChoiceInline]
    exclude           = ['submitter']
    
    def ald_issues(self, obj):
        """
        Formatted issue list for admin list_display option."
        
        """
        issues = [issue.number for issue in obj.issues.all()]
        return ', '.join(['%s' % issue for issue in issues])

    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        
        Auto-save submitter.
        
        """
        if change == False:
            obj.submitter = request.user
        obj.save()

admin.site.register(Poll, PollAdmin)
custom_site.register(Poll, PollAdmin)



class ChoiceAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Choice`` model.
    
    """
    list_display  = ('poll', 'choice')
    list_filter   = ('poll',)
    search_fields = ('choice',)

admin.site.register(Choice, ChoiceAdmin)
custom_site.register(Choice, ChoiceAdmin)



class VoteAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Vote`` model.
    
    """
    list_display      = ('poll', 'choice', 'creation_date', 'ip_address')
    list_filter       = ('poll',)
    search_fields     = ('poll', 'choice', 'ip_address')
    ordering          = ('-creation_date',)
    date_hierarchy    = 'creation_date'
    
admin.site.register(Vote, VoteAdmin)
custom_site.register(Vote, VoteAdmin)


