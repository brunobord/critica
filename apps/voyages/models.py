# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.voyages`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import BaseArticle
from critica.apps.voyages.managers import PublishedArticleManager
from critica.apps.utils.widgets import resize_widget


class VoyagesArticle(BaseArticle):
    """
    Voyages article category: article.
    
    Database table name: ``voyages_article``.
    
    Fields::
    
        See BaseArticle. And below.
        
        localization
            * CharField
            * 255 characters max.
            * The localization
            * Required
            
        widget
            * TextField
            * The video widget
            * Required
            
    Indexes::
    
        See BaseArticle. And below.
        
        * localization
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
        
        published
            Only returns ready to publish articles.
            Manager: critica.apps.voyages.managers.PublishedArticleManager()
    
    """
    localization = models.CharField(_('localization'), max_length=255, db_index=True, help_text=_('Please, enter the localization in this format: city, country (e.g. Paris, France).'))
    widget       = models.TextField(_('Google Map widget'), help_text=_('Please, copy-paste the widget here. Do not modify it.'))
    
    objects = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'voyages_article'
        verbose_name = _('article voyage')
        verbose_name_plural = _('articles voyage')
        
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Auto-save category
        * Resize widget
        * Save article
        
        """
        from critica.apps.categories.models import Category
        category = Category.objects.get(slug='voyages')
        self.category = category
        new_widget = resize_widget(self.widget, 300, 300)
        self.widget = new_widget
        super(VoyagesArticle, self).save()


