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
        # Auto-creates categories
        if 'critica.apps.categories' in settings.INSTALLED_APPS:
            from critica.apps.categories.models import Category, CategoryPosition
            categories = Category.objects.all()
            for category in categories:
                category_position = CategoryPosition(issue=self, category=category)
                category_position.save()
        # Auto-creates note types
        if 'critica.apps.notes' in settings.INSTALLED_APPS:
            from critica.apps.notes.models import NoteType, NoteTypePosition
            note_types = NoteType.objects.all()
            for note_type in note_types:
                note_type_position = NoteTypePosition(issue=self, type=note_type)
                note_type_position.save()


