# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.articles`` models. 

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.articles.models import Article


class BaseArticleAdmin(admin.ModelAdmin):
    """
    Administration interface for ``BaseArticle`` abstract model.
    
    """
    list_display = ('title', 'category', 'ald_issues', 'tags', 'ald_publication_date', 'ald_opinion', 'is_featured', 'ald_author', 'ald_author_nickname', 'view_count', 'status')
    list_filter = ('author', 'status', 'is_featured', 'category')
    search_fields = ('title', 'content')
    radio_fields = {'status': admin.VERTICAL}
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    exclude = ['author']
    
    class Media:
        """
        Model metadata.
        
        """
        js = (
            settings.MEDIA_URL + 'common/js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'common/js/textarea.js',
        )

    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        Auto-save author.
        
        """
        obj.author = request.user
        obj.save()
        
    def get_form(self, request, obj=None, **kwargs):
        """
        Returns a Form class for use in the admin add view. This is used by
        add_view and change_view.
        
        Excludes fields depending on user permissions.
        
        """
        exclude = []
        #if not request.user.has_perm('users.can_reserve_article'):
        #    exclude.append('is_reserved')
        if not request.user.has_perm('users.can_feature_article'):
            exclude.append('is_featured')
        defaults = {'exclude': exclude}
        defaults.update(kwargs)
        return super(BaseArticleAdmin, self).get_form(request, obj, **defaults)


class ArticleAdmin(BaseArticleAdmin):
    """
    Administration interface for ``Article`` model.
    
    """
    fieldsets = (
        (_('Headline'), 
            {'fields': ('author_nickname', 'title', 'opinion', 'is_featured')}
        ),
        (_('Filling'),
            {'fields': ('issues', 'category', 'tags')},
        ),
        (_('Illustration'),
            {'fields': ('illustration', 'use_default_illustration')}
        ),
        (_('Content'),
            {'fields': ('summary', 'content')}
        ),
        (_('Publication'),
            {'fields': ('publication_date', 'status')}
        ),
    )
    search_fields = ('title', 'summary', 'content')

    def get_form(self, request, obj=None, **kwargs):
        exclude = []
        if not request.user.has_perm('users.can_validate_illustration'):
            exclude.append('is_illustrated')
        defaults = {'exclude': exclude}
        defaults.update(kwargs)
        return super(ArticleAdmin, self).get_form(request, obj, **defaults)

basic_site.register(Article, ArticleAdmin)
advanced_site.register(Article, ArticleAdmin)

