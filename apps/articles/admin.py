# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.articles`` application.

"""
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.articles.models import Article
from critica.apps.users.models import UserNickname
from critica.apps.categories.models import Category
from critica.apps.illustrations.models import Illustration
from critica.apps.articles import settings as articles_settings


class BaseArticleAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``BaseArticle`` abstract model.
    
    """
    list_display = ('title', 'category', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'view_count', 'is_featured', 'is_reserved', 'is_ready_to_publish', 'ald_illustration')
    list_filter = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'category')
    search_fields = ('title', 'summary', 'content')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    exclude = ['author']
    
    def __call__(self, request, url):
        self.request = request
        return super(BaseArticleAdmin, self).__call__(request, url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(BaseArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        current_user = self.request.user
        if db_field.name == 'author_nickname': 
            my_choices = [('', '---------')]
            my_choices.extend(UserNickname.objects.filter(user=current_user).values_list('id','nickname'))
            print my_choices
            field.choices = my_choices
        if db_field.name == 'illustration':
            my_choices = [('', '---------')]
            if 'users.is_editor' in current_user.get_all_permissions():
                my_choices.extend(Illustration.objects.all().values_list('id','legend'))
            else:
                my_choices.extend(Illustration.objects.filter(submitter=self.request.user).values_list('id','legend'))
            print my_choices
            field.choices = my_choices
        if db_field.name == 'category':
            my_choices = [('', '---------')]
            my_choices.extend(Category.objects.exclude(slug__in=articles_settings.EXCLUDED_CATEGORIES).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field

    def queryset(self, request):
        """ 
        Ability for a user to edit only objects he/she has created (except for superuser). 
        
        """
        qs = super(BaseArticleAdmin, self).queryset(request)
        user = request.user
        if user.is_superuser or user.has_perm('users.is_administrator') or user.has_perm('users.is_editor'):
            return qs
        else:
            return qs.filter(author=user)
        
    def get_fieldsets(self, request, obj=None):
        """ 
        Hook for specifying fieldsets for the add form. 
        
        """
        publication_fields = []
        publication_fields.append('is_featured')
        publication_fields.append('is_reserved')
        if request.user.has_perm('users.is_editor'):
            publication_fields.append('is_ready_to_publish')
        fieldsets = [
            (_('Headline'), {'fields': ('author_nickname', 'title', 'opinion', 'publication_date')}),
            (_('Filling'), {'fields': ('issues', 'category', 'tags')}),
            (_('Illustration'), {'fields': ('illustration', 'use_default_illustration')}),
            (_('Content'), {'fields': ('summary', 'content')}),
            (_('Publication'), {'fields': publication_fields}),
        ]
        return fieldsets


    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        Auto-save author.
        
        """
        obj.author = request.user
        obj.save()
        
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
            return obj.publication_date.strftime('%Y/%m/%d')
    ald_publication_date.short_description = _('publication date')
    ald_publication_date.allow_tags = True
    
    def ald_illustration(self, obj):
        """
        Illustration thumbnail for admin list_display option.
        
        """
        if obj.use_default_illustration:
            thumb = '<img src="%s%s" alt="%s" height="50" class="default-illustration" />' % (settings.MEDIA_URL, obj.category.image, obj.category.image_legend)
        else:
            thumb = '<img src="%s%s" alt="%s" height="50" />' % (settings.MEDIA_URL, obj.illustration.image, obj.illustration.legend)
        return thumb
    ald_illustration.allow_tags = True
    ald_illustration.short_description = _('Illustration')


class ArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``Article`` model.
    
    """
    pass

admin.site.register(Article, ArticleAdmin)
basic_site.register(Article, ArticleAdmin)
advanced_site.register(Article, ArticleAdmin)

