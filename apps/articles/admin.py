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

    def ald_author(self, obj):
        """
        Formatted author for admin list_display option.
        
        """
        if obj.author.get_full_name():
            return obj.author.get_full_name()
        else:
            return obj.author
    ald_author.short_description = _('author')
    
    def ald_author_nickname(self, obj):
        """
        Formatted author nickname for admin list_display option.
        
        """
        if obj.author_nickname:
            return obj.author_nickname
        else:
            return self.ald_author(obj)
    ald_author_nickname.short_description = _('author nickname')

    def ald_issues(self, obj):
        """
        Formatted issue list for admin list_display option."
        
        """
        issues = [issue.number for issue in obj.issues.all()]
        return ', '.join(['%s' % issue for issue in issues])
    ald_issues.short_description = _('issues')

    def ald_opinion(self, obj):
        """
        Formatted opinion for admin list_display option.
        
        """
        if obj.opinion:
            return obj.opinion
        else:
            return u'<span class="novalue">%s</span>' % _('no opinion')
    ald_opinion.short_description = _('opinion')
    ald_opinion.allow_tags = True
    
    def ald_publication_date(self, obj):
        """
        Formatted publication date for admin list_display option.
        
        """
        if not obj.publication_date:
            return u'<span class="novalue">%s</span>' % _('no publication date')
        else:
            return obj.publication_date
    ald_publication_date.short_description = _('publication date')
    ald_publication_date.allow_tags = True
    
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

