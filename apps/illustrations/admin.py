# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.illustrations`` models. 

"""
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.illustrations.models import Illustration, IllustrationOfTheDay
from critica.apps.issues.models import Issue


class IllustrationAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Illustration`` model.
    
    """
    fieldsets = [
        (None, {'fields': ('category', 'image', 'credits', 'legend')}),
    ]
    
    list_display = ('ald_image', 'ald_category', 'credits', 'legend', 'creation_date', 'modification_date', 'submitter')
    list_filter = ('category',)
    search_fields = ('image', 'credits', 'legend')
    ordering = ['-creation_date']
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
    
    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        Auto-save author.
        
        """
        obj.submitter = request.user
        obj.save()

admin.site.register(Illustration, IllustrationAdmin)
basic_site.register(Illustration, IllustrationAdmin)
advanced_site.register(Illustration, IllustrationAdmin)


class IllustrationOfTheDayAdmin(admin.ModelAdmin):    
    """
    Administration interface options of ``IllustrationOfTheDay`` model.
    
    """
    fieldsets = [
        (None, {'fields': ('image', 'credits', 'legend', 'issues')}),
    ]
    
    list_display = ('ald_image', 'ald_issues', 'credits', 'legend', 'creation_date', 'modification_date', 'submitter')
    list_filter = ('issues',)
    filter_horizontal = ['issues']
    search_fields = ('image', 'credits', 'legend', 'issues__number')
    ordering = ['issues', 'legend', 'creation_date']
    date_hierarchy = 'creation_date'
    _object = None

    def __call__(self, request, url):
        self.request = request
        return super(IllustrationOfTheDayAdmin, self).__call__(request, url)

    def change_view(self, request, object_id):
        self._request = request
        self._object = None
        try:
            self._object = self.model._default_manager.get(pk=object_id)
        except model.DoesNotExist:
            self._object = None
        self._action = "change"
        return super(IllustrationOfTheDayAdmin, self).change_view(request, object_id) 

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(IllustrationOfTheDayAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'issues': 
            my_choices = []
            # Displays only available issues
            issues = []
            illustrations = IllustrationOfTheDay.objects.all()
            for illustration in illustrations:
                for issue in illustration.issues.all():
                    issues.append((issue.id, issue))
            all_issues = list(set(issues))        
            excluded_issues = [int(issue.id) for issue_id, issue in all_issues]
            if self._object is not None:
                current_issues = [int(issue.id) for issue in self._object.issues.all()]
                for current_issue in current_issues:
                    excluded_issues.remove(current_issue)
            my_choices.extend(Issue.objects.exclude(id__in=excluded_issues).values_list('id', 'number'))
            print my_choices
            field.choices = my_choices
        return field

    def ald_issues(self, obj):
        """
        Formatted issue list for admin list_display option."
        
        """
        if obj.issues.all():
            issues = [issue.number for issue in obj.issues.all()]
            return ', '.join(['%s' % issue for issue in issues])
        else:
            return _('no issues')
    ald_issues.short_description = _('issues')
    
    def ald_image(self, obj):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, obj.image, obj.legend)
    ald_image.allow_tags = True
    ald_image.short_description = _('Illustration')
    
    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        Auto-save author.
        
        """
        obj.submitter = request.user
        obj.save()

admin.site.register(IllustrationOfTheDay, IllustrationOfTheDayAdmin)
basic_site.register(IllustrationOfTheDay, IllustrationOfTheDayAdmin)
advanced_site.register(IllustrationOfTheDay, IllustrationOfTheDayAdmin)

