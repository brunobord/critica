# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.issues`` application.

"""
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from critica.apps.issues.managers import PublishedIssueManager
from critica.apps.utils import urlbase64


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
            
        secret_key
            * CharField
            * The issue secret key
            * Optional (can be blank)
            
        is_published
            * BooleanField
            * Default: False
            * Is issue ready to be published?
            * Required
    
    Indexes::
    
        * number
        * secret_key
        * is_published
    
    Managers::
    
        objects
            Default manager: models.Manager()
        
        published
            Published issues: critica.apps.issues.managers.PublishedIssueManager()

    """
    number = models.PositiveIntegerField(_('number'), unique=True, help_text=_("Please, enter the issue's number."))
    publication_date = models.DateField(_('publication date'), null=True, blank=True, help_text=_("Don't forget to adjust the publication date"))
    secret_key = models.CharField(_('secret key'), max_length=30, blank=True, db_index=True, editable=False)
    is_published = models.BooleanField(_('published'), default=False)
    
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
        
    def get_preview_url(self):
        """
        Returns issue preview secret URL.
        
        """
        return u'/%s/%s/' % ('preview', self.secret_key)
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates "secret" key
        * Save issue
        
        """
        self.secret_key = urlbase64.uri_b64encode(str(self.number))
        super(Issue, self).save()


