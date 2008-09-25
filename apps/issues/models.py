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
        from apps.categories.models import Category
        from apps.positions.models import CategoryPosition
        from apps.positions import settings as positions_settings
        # Auto-creates categories
        if 'critica.apps.categories' in settings.INSTALLED_APPS:
            for slug in positions_settings.CATEGORY_DEFAULT_ORDER:
                # defining default position if it does exist
                if slug in positions_settings.CATEGORY_DEFAULT_POSITION:
                    default_position = positions_settings.CATEGORY_DEFAULT_POSITION[slug]
                else:
                    default_position = None

                # the category must exist
                category = Category.objects.get(slug=slug)
                # create the category
                position = CategoryPosition(issue=self,
                    category=category,
                    position=default_position,
                )
                position.save()

