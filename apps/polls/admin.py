# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.polls`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.issues.models import Issue
from critica.apps.polls.models import Poll
from critica.apps.polls.models import Choice
from critica.apps.polls.models import Vote
from critica.apps.polls.forms import PollAdminModelForm


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
    list_display = ('title', 'ald_issues', 'creation_date', 'modification_date', 'is_published', 'submitter')
    list_filter = ('issues', 'is_published', 'submitter')
    filter_horizontal = ('issues',)
    search_fields = ('title',)
    ordering = ('-creation_date',)
    date_hierarchy = 'creation_date'
    inlines = [ChoiceInline]
    exclude = ['submitter']
    form = PollAdminModelForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(PollAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'issues': 
            my_choices = [('', '---------')]
            my_choices.extend(Issue.objects.order_by('-number').values_list('id','number'))
            print my_choices
            field.choices = my_choices
        return field

    def ald_issues(self, obj):
        """
        Formatted issue list for admin list_display option."
        
        """
        issues = [issue.number for issue in obj.issues.all()]
        return ', '.join(['%s' % issue for issue in issues])
    ald_issues.short_description = _('issues')

    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        
        """
        if change == False:
            obj.submitter = request.user
        obj.save()


class ChoiceAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Choice`` model.
    
    """
    list_display  = ('poll', 'choice')
    list_filter   = ('poll',)
    search_fields = ('choice',)


class VoteAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Vote`` model.
    
    """
    list_display      = ('poll', 'choice', 'creation_date', 'ip_address')
    list_filter       = ('poll',)
    search_fields     = ('poll', 'choice', 'ip_address')
    ordering          = ('-creation_date',)
    date_hierarchy    = 'creation_date'
    

# Registers
# ------------------------------------------------------------------------------
admin.site.register(Poll, PollAdmin)
custom_site.register(Poll, PollAdmin)

admin.site.register(Choice, ChoiceAdmin)
custom_site.register(Choice, ChoiceAdmin)

admin.site.register(Vote, VoteAdmin)
custom_site.register(Vote, VoteAdmin)
