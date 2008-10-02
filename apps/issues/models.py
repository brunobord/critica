# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.issues`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.issues import choices
from critica.apps.issues.managers import PublishedIssueManager


class Issue(models.Model):
    """
    Issue.
    
    Database table name: ``issues_issue``.
    
    An issue is composed of::
    
        number
            * PositiveIntegerField
            * The issue number
            * Must be unique
            * Required
            
        publication_date
            * DateField
            * The issue publication date
            * Optional (can be blank)
            
        status
            * IntegerField
            * Choices: critica.apps.issues.choices.STATUS_CHOICES
            * Default: critica.apps.issues.choices.STATUS_NEW
            * The issue status
            * Required
    
    Indexes::
    
        * number
        * status
    
    Managers::
    
        objects
            Default manager: models.Manager()
        
        published
            Published issues: critica.apps.issues.managers.PublishedIssueManager()

    """
    number = models.PositiveIntegerField(_('number'), unique=True, help_text=_("Please, enter the issue's number."))
    publication_date = models.DateField(_('publication date'), null=True, blank=True, help_text=_("Don't forget to adjust the publication date"))
    status = models.IntegerField(_('status'), choices=choices.STATUS_CHOICES, default=choices.STATUS_NEW, db_index=True, help_text=_('Please, select a status.'))
    
    objects = models.Manager()
    published = PublishedIssueManager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('issue')
        verbose_name_plural = _('issues')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.number
    
    def save(self):
        super(Issue, self).save()
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
                position = CategoryPosition(issue=self, category=category, position=default_position)
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
                    position = NoteTypePosition(issue=self, category=category, type=note_type, position=default_position)
                    position.save()
                    
        if 'critica.apps.quotas' in settings.INSTALLED_APPS:
            from critica.apps.quotas.models import DefaultCategoryQuota
            from critica.apps.quotas.models import CategoryQuota
            default_quotas = DefaultCategoryQuota.objects.all()
            for default_quota in default_quotas:
                category = Category.objects.get(slug=default_quota.category.slug)
                category_quota = CategoryQuota(issue=self, category=category, quota=default_quota.quota)
                category_quota.save()


