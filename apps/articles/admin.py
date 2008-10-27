# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.articles`` application.

"""
from django.conf import settings
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from critica.apps.custom_admin.sites import custom_site
from critica.apps.articles.models import Article
from critica.apps.users.models import UserNickname
from critica.apps.categories.models import Category
from critica.apps.issues.models import Issue
from critica.apps.articles import settings as articles_settings
from critica.lib.widgets import ImageWithThumbWidget

from imagethumbnail.templatetags.image_thumbnail import thumbnail


class BaseArticleAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``BaseArticle`` abstract model.
    
    """
    list_display      = ('title', 'category', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish', 'ald_image')
    list_filter       = ('issues', 'author', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'category')
    filter_horizontal = ('issues',)
    search_fields     = ('title', 'summary', 'content')
    ordering          = ('-publication_date', 'category')
    date_hierarchy    = 'publication_date'
    exclude           = ['author']

    
    def __call__(self, request, url):
        """
        Adds current request object and current URL to this class.
        
        """
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
            if not current_user.has_perms('users.is_editor'):
                my_choices.extend(UserNickname.objects.all().values_list('id','nickname'))
            else:
                my_choices.extend(UserNickname.objects.filter(user=current_user).values_list('id','nickname'))
            print my_choices
            field.choices = my_choices
            
        if db_field.name == 'category':
            my_choices = [('', '---------')]
            my_choices.extend(Category.objects.exclude(slug__in=articles_settings.EXCLUDED_CATEGORIES).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        
        if db_field.name == 'image':
            return forms.ImageField(widget=ImageWithThumbWidget(), label=_('Image'), help_text=_('You can attach an image to this article. By default, the category image is displayed.'), required=False) 
        
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
            (_('Image'), {'fields': ('image', 'image_legend', 'image_credits')}),
            (_('Content'), {'fields': ('summary', 'content')}),
            (_('Publication'), {'fields': publication_fields}),
        ]
        return fieldsets


    def save_model(self, request, obj, form, change):
        """ 
        Given a model instance save it to the database. 
        
        Auto-save author.
        
        """
        if change == False:
            obj.author = request.user
        obj.save()

    
    def ald_author(self, obj):
        """
        Formatted author for admin list_display option.
        
        """
        if obj.author_nickname:
            return obj.author_nickname.nickname
        else:
            if obj.author.get_full_name():
                return obj.author.get_full_name()
            else:
                return obj.author.username
    
    ald_author.short_description = 'auteur'


    def ald_issues(self, obj):
        """
        Formatted issue list for admin list_display option."
        
        """
        issues = [issue.number for issue in obj.issues.all()]
        return ', '.join(['%s' % issue for issue in issues])
    
    ald_issues.short_description = 'édition(s)'


    def ald_opinion(self, obj):
        """
        Formatted opinion for admin list_display option.
        
        """
        from critica.apps.articles import choices
        if obj.opinion:
            for opinion in choices.OPINION_CHOICES:
                if obj.opinion == opinion[0]:
                    return opinion[1]
        else:
            return u'<span class="novalue">%s</span>' % _('no opinion')
    
    ald_opinion.short_description = 'opinion'
    ald_opinion.allow_tags = True


    def ald_publication_date(self, obj):
        """
        Formatted publication date for admin list_display option.
        
        """
        if not obj.publication_date:
            return u'<span class="novalue">%s</span>' % _('no publication date')
        else:
            return obj.publication_date.strftime('%Y/%m/%d')
    
    ald_publication_date.short_description = 'date'
    ald_publication_date.allow_tags = True


    def ald_image(self, obj):
        """
        Image thumbnail for admin list_display option.
        
        """
        if not obj.image:
            img_thumb = thumbnail(obj.category.image, '45,0')
            thumb = '<div class="default-illustration"><img src="%s" alt="%s" /></div>' % (img_thumb, obj.category.image_legend)
        else:
            img_thumb = thumbnail(obj.image, '45,0')
            thumb = '<img src="%s" alt="%s" />' % (img_thumb, obj.image_legend)
        return thumb
    
    ald_image.allow_tags = True
    ald_image.short_description = 'visuel'


    def ald_view_count(self, obj):
        return obj.view_count
    
    ald_view_count.short_description = 'nb vues'

    
    def ald_is_reserved(self, obj):
        return obj.is_reserved
    
    ald_is_reserved.short_description = 'marbre'
    ald_is_reserved.boolean = True
    


class ArticleAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``Article`` model.
    
    """
    pass

admin.site.register(Article, ArticleAdmin)
custom_site.register(Article, ArticleAdmin)

