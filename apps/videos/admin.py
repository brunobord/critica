# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.videos`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.videos.models import Video
from critica.apps.issues.models import Issue


class VideoAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Video`` model.
    
    """
    fieldsets = (
        (_('Video'), {'fields': ('name', 'widget')}),
        (_('Filling'), {'fields': ('issues', 'tags')}),
        (_('Publication'), {'fields': ('is_reserved', 'is_ready_to_publish')}),
    )
    list_display = ('name', 'ald_issues', 'creation_date', 'modification_date', 'is_reserved', 'is_ready_to_publish', 'ald_submitter')
    list_filter = ('issues',)
    filter_horizontal = ('issues',)
    search_fields = ('name',)
    ordering = ('-creation_date',)
    date_hierarchy = 'creation_date'
    exclude = ['author']
    _object = None
    
    def __call__(self, request, url):
        self.request = request
        return super(VideoAdmin, self).__call__(request, url)

    def change_view(self, request, object_id):
        self._request = request
        self._object = None
        try:
            self._object = self.model._default_manager.get(pk=object_id)
        except model.DoesNotExist:
            self._object = None
        self._action = "change"
        return super(VideoAdmin, self).change_view(request, object_id) 

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(VideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'issues': 
            my_choices = []
            # Displays only available issues
            issues = []
            videos = Video.objects.all()
            for video in videos:
                for issue in video.issues.all():
                    issues.append((issue.id, issue))
            all_issues = list(set(issues))        
            excluded_issues = [int(issue.id) for issue_id, issue in all_issues]
            if self._object:
                current_issues = [int(issue.id) for issue in self._object.issues.all()]
                for current_issue in current_issues:
                    excluded_issues.remove(current_issue)
            my_choices.extend(Issue.objects.exclude(id__in=excluded_issues).values_list('id', 'number'))
            print my_choices
            field.choices = my_choices
        return field
        
    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        Auto-save submitter.
        
        """
        obj.submitter = request.user
        obj.save()

    def ald_submitter(self, obj):
        """
        Formatted submitter for admin list_display option.
        
        """
        if obj.submitter.get_full_name():
            return obj.submitter.get_full_name()
        else:
            return obj.submitter
    ald_submitter.short_description = _('submitter')

    def ald_issues(self, obj):
        """
        Formatted issue list for admin list_display option."
        
        """
        issues = [issue.number for issue in obj.issues.all()]
        return ', '.join(['%s' % issue for issue in issues])
    ald_issues.short_description = _('issues')

admin.site.register(Video, VideoAdmin)
basic_site.register(Video, VideoAdmin)
advanced_site.register(Video, VideoAdmin)

