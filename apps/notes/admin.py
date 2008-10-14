# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.notes`` application.

"""
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.notes.models import NoteType, Note
from critica.apps.articles.admin import BaseArticleAdmin
from critica.apps.users.models import UserNickname
from critica.apps.categories.models import Category
from critica.apps.issues.models import Issue
from critica.apps.notes import settings as notes_settings


class NoteTypeAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``NoteType`` model.
    
    """
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    ordering = ['name']

admin.site.register(NoteType, NoteTypeAdmin)
basic_site.register(NoteType, NoteTypeAdmin)
advanced_site.register(NoteType, NoteTypeAdmin)


class BaseNoteAdmin(BaseArticleAdmin):
    """
    Administration interface options of ``BaseNote`` abstract model.
    
    """
    list_display = ('title', 'category', 'type', 'ald_issues', 'ald_publication_date', 'ald_opinion', 'ald_author', 'ald_author_nickname', 'ald_view_count', 'is_featured', 'ald_is_reserved', 'is_ready_to_publish')
    list_filter = ('issues', 'author', 'type', 'is_ready_to_publish', 'is_reserved', 'opinion', 'is_featured', 'category')
    filter_horizontal = ('issues',)
    search_fields = ('title', 'content')
    ordering = ('-publication_date', 'category')
    date_hierarchy = 'publication_date'
    exclude = ['author']

    def __call__(self, request, url):
        self.request = request
        return super(BaseNoteAdmin, self).__call__(request, url)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(BaseNoteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'author_nickname': 
            my_choices = [('', '---------')]
            my_choices.extend(UserNickname.objects.filter(user=self.request.user).values_list('id','nickname'))
            print my_choices
            field.choices = my_choices
        if db_field.name == 'issues': 
            my_choices = []
            my_choices.extend(Issue.objects.all().values_list('id','number')[:15])
            print my_choices
            field.choices = my_choices
        if db_field.name == 'category':
            my_choices = [('', '---------')]
            my_choices.extend(Category.objects.exclude(slug__in=notes_settings.EXCLUDED_CATEGORIES).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field

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
            (_('Filling'), {'fields': ('issues', 'category', 'type', 'tags')}),
            (_('Content'), {'fields': ('content',)}),
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
    ald_author_nickname.short_description = 'pseudo'

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
    ald_publication_date.short_description = 'date'
    ald_publication_date.allow_tags = True
    
    def ald_view_count(self, obj):
        return obj.view_count
    ald_view_count.short_description = 'nb vues'
    
    def ald_is_reserved(self, obj):
        return obj.is_reserved
    ald_is_reserved.short_description = 'marbre'
    ald_is_reserved.boolean = True
    

class NoteAdmin(BaseNoteAdmin):
    """
    Administration interface options of ``Note`` model.
    
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance. If kwargs are given, they're passed to the form Field's constructor.
        
        """
        field = super(NoteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'type': 
            my_choices = [('', '---------')]
            type_order = notes_settings.TYPE_ORDER
            for slug in type_order:
                my_choices.extend(NoteType.objects.filter(slug=slug).values_list('id','name'))
            print my_choices
            field.choices = my_choices
        return field

admin.site.register(Note, NoteAdmin)
basic_site.register(Note, NoteAdmin)
advanced_site.register(Note, NoteAdmin)

