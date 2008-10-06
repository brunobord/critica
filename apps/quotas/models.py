# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.quotas`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DefaultCategoryQuota(models.Model):
    """
    Default category quota.
    
    Fields::
        
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Required
            
        quota
            * IntegerField
            * The default category quota
            * Required
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
            
    Indexes::
    
        * category
        * quota
    
    """
    category = models.ForeignKey('categories.Category', verbose_name=_('category'), unique=True, help_text=_('Please, select a category.'))
    quota = models.IntegerField(_('quota'), help_text=_('Please, enter the default quota for this category.'))
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'quotas_defaultcategoryquota'
        verbose_name = _('default category quota')
        verbose_name_plural = _('default category quotas')
    
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s - %s' % (self.category, self.quota)
        
    
    
class CategoryQuota(models.Model):
    """
    Category quota.
    
    Fields::
        
        issue
            * ForeignKey: critica.apps.issues.models.Issue
            * The issue
            * Required
            
        category
            * ForeignKey: critica.apps.categories.models.Category
            * The category
            * Required
        
        quota
            * IntergerField
            * The quota
            * Required
            
    Managers::
        
        objects
            Default manager.
            Manager: models.Manager()
            
    Indexes::
    
        * category
        * quota
        * issue / category / quota
    
    """
    issue = models.ForeignKey('issues.Issue', verbose_name=_('issue'))
    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    quota = models.IntegerField(_('quota'), help_text=_('Please, enter the article quota for this category.'))
    
    objects = models.Manager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'quotas_categoryquota'
        verbose_name = _('category quota')
        verbose_name_plural = _('category quotas')
        unique_together = (('issue', 'category', 'quota'),)

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s - %s' % (self.category, self.quota)

