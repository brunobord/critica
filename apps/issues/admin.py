# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue
    
    
class IssueAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Issue`` model.
    
    """
    list_display = ('number', 'publication_date', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    date_hierarchy = 'publication_date'

    def save_model(self, request, obj, form, change):
        obj.save()
        if change == False:
            from django.conf import settings
            from critica.apps.positions import settings as positions_settings
            from critica.apps.categories.models import Category
            if 'critica.apps.categories' in settings.INSTALLED_APPS:
                from critica.apps.positions.models import CategoryPosition
                for slug in positions_settings.CATEGORY_DEFAULT_ORDER:
                    # defining default position if it does exist
                    if slug in positions_settings.CATEGORY_DEFAULT_POSITION:
                        default_position = positions_settings.CATEGORY_DEFAULT_POSITION[slug]
                    else:
                        default_position = None
                    # the category must exist
                    category = Category.objects.get(slug=slug)
                    # create the category
                    position = CategoryPosition(issue=obj, category=category, position=default_position)
                    position.save()
            if 'critica.apps.notes' in settings.INSTALLED_APPS: 
                from critica.apps.notes.models import NoteType
                from critica.apps.positions.models import NoteTypePosition
                categories = Category.objects.exclude(slug__in=positions_settings.EXCLUDED_CATEGORIES)
                for category in categories:
                    for slug in positions_settings.NOTE_TYPE_DEFAULT_ORDER:
                        if slug in positions_settings.NOTE_TYPE_DEFAULT_POSITION:
                            default_position = positions_settings.NOTE_TYPE_DEFAULT_POSITION[slug]
                        else:
                            default_position = None
                        note_type = NoteType.objects.get(slug=slug)
                        position = NoteTypePosition(issue=obj, category=category, type=note_type, position=default_position)
                        position.save() 
            if 'critica.apps.quotas' in settings.INSTALLED_APPS:
                from critica.apps.quotas.models import DefaultCategoryQuota
                from critica.apps.quotas.models import CategoryQuota
                default_quotas = DefaultCategoryQuota.objects.all()
                for default_quota in default_quotas:
                    category = Category.objects.get(slug=default_quota.category.slug)
                    category_quota = CategoryQuota(issue=obj, category=category, quota=default_quota.quota)
                    category_quota.save()

admin.site.register(Issue, IssueAdmin)
basic_site.register(Issue, IssueAdmin)
advanced_site.register(Issue, IssueAdmin)


