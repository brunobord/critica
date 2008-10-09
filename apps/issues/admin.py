# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue
    
    
class IssueAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Issue`` model.
    
    """
    list_display = ('number', 'publication_date', 'ald_secret_link', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    date_hierarchy = 'publication_date'
    
    def ald_secret_link(self, obj):
        site = Site.objects.get_current()
        url = 'http://%s/preview/%s/' % (site.domain, obj.secret_key)
        return '<a href="%s">%s</a>' % (url, url)
    ald_secret_link.allow_tags = True
    ald_secret_link.short_description = _('secret link')

    def save_model(self, request, obj, form, change):
        obj.save()
        if change == False:
            from django.conf import settings
            if 'critica.apps.categories' in settings.INSTALLED_APPS:
                from critica.apps.positions.models import DefaultCategoryPosition
                from critica.apps.positions.models import IssueCategoryPosition
                default_positions = DefaultCategoryPosition.objects.all()
                for default_position in default_positions:
                    issue_position = IssueCategoryPosition(
                        issue=obj, 
                        category=default_position.category, 
                        position=default_position.position)
                    issue_position.save()
            if 'critica.apps.notes' in settings.INSTALLED_APPS:
                from critica.apps.positions.models import DefaultNotePosition
                from critica.apps.positions.models import IssueNotePosition
                default_positions = DefaultNotePosition.objects.all()
                for default_position in default_positions:
                    issue_position = IssueNotePosition(
                        issue=obj,
                        category=default_position.category,
                        type=default_position.type,
                        position=default_position.position)
                    issue_position.save()
            if 'critica.apps.quotas' in settings.INSTALLED_APPS:
                from critica.apps.categories.models import Category
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


