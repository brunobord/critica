# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.journal``.

"""
from datetime import datetime
from django.db import models
from django.conf import settings
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.models import Tag
from tagging.fields import TagField
from critica.apps.journal import choices
from critica.apps.journal.managers import CategoryManager
from critica.apps.journal.managers import IllustrationManager
from critica.apps.journal.managers import ReportageManager
from critica.apps.journal.managers import ArticleManager
from critica.apps.journal.managers import IssueManager


# Category
# ------------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(_('name'), max_length=255, help_text=_('As short as possible.'))
    slug = models.SlugField(_('URL'), max_length=255, blank=True, unique=True, editable=False)
    description = models.CharField(_('description'), max_length=255, blank=True, help_text=_('A short description of the category. It will not be displayed on the website.'))
    image = models.ImageField(upload_to='upload/categories/', max_length=200, help_text=_('Please, upload an image for this category (it will be used as default category illustration).'))
    image_credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    image_legend = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = CategoryManager()
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return u'%s' % self.name

    def formatted_slug(self):
        return 'http://www.critica.fr/<strong>%s</strong>/' % (self.slug)
    formatted_slug.allow_tags = True
    formatted_slug.short_description = _('URL')
    
    def image_thumbnail(self):
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.image_legend)
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = _('Default illustration')

    @permalink
    def get_absolute_url(self):
        return ('category', (), {
            'slug': self.slug,
        })
        
    def get_rss_url(self):
        return u'/rss/rubriques/%s/' % self.slug

    def _get_complete_articles(self):
        return self.article_set.filter(is_published=True, is_reserved=False)
    complete_article_set = property(_get_complete_articles)

    def save(self):
        """ Object pre-saving operations. """
        self.slug = slugify(self.name)
        super(Category, self).save()


# Illustration
# ------------------------------------------------------------------------------
class Illustration(models.Model):
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    image = models.ImageField(upload_to='critica/upload/%Y/%m/%d', max_length=200, help_text=_('Please, select an image to upload'))
    credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    category = models.ForeignKey(Category, verbose_name=_('category'), null=True, blank=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = IllustrationManager()
    
    class Meta:
        verbose_name = _('illustration')
        verbose_name_plural = _('illustrations')

    def __unicode__(self):
        return u'%s' % self.image

    def thumbnail(self):
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.legend)
    thumbnail.allow_tags = True
    thumbnail.short_description = _('Illustration')

    def bolded_category(self):
        return '<strong>%s</strong>' % (self.category,)
    bolded_category.allow_tags = True
    bolded_category.short_description = _('Category')


# Reportage
# ------------------------------------------------------------------------------
class Reportage(models.Model):
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    video_name = models.CharField(_('video name'), max_length=255, help_text=_('Please, enter a name for this video.'))
    video_link = models.CharField(_('video link'), max_length=255, help_text=_('Please, enter the video URL.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    is_published = models.BooleanField(_('published'), default=False, help_text=_('Is video ready to be published?'))
    
    objects = models.Manager()
    published = ReportageManager()
    
    class Meta:
        verbose_name = _('reportage')
        verbose_name_plural = _('reportages')

    def __unicode__(self):
        return u'%s' % self.video_name


# Issue
# ------------------------------------------------------------------------------
class Issue(models.Model):
    number = models.PositiveIntegerField(_('number'), unique=True, help_text=_("Please, enter the issue's number."))
    publication_date = models.DateTimeField(_('publication date'), blank=True, help_text=_("Don't forget to adjust the publication date"))
    is_complete = models.BooleanField(_('complete'), default=False, db_index=True, help_text=_('Is issue complete'))
    
    objects = models.Manager()
    complete = IssueManager()
    
    class Meta:
        verbose_name = _('issue')
        verbose_name_plural = _('issues')

    def __unicode__(self):
        return u'%s' % self.number

    def _get_complete_articles(self):
        return self.article_set.filter(is_published=True, is_illustrated=True, is_reserved=False)
    complete_article_set = property(_get_complete_articles)


# Articles: article / note
# ------------------------------------------------------------------------------
class BaseArticle(models.Model):
    author = models.ForeignKey('auth.User', verbose_name=_('author'), help_text=_('Please, select an author for this article.'))
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    category = models.ForeignKey(Category, verbose_name=_('category'), help_text=_('Please, select a category for this article.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    issues = models.ManyToManyField(Issue, verbose_name=_('issues'), help_text=_('Please, select one or several issues.'))
    view_count = models.PositiveIntegerField(_('view count'), null=True, blank=True, editable=False)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date = models.DateTimeField(_('publication date'), blank=True, help_text=_("Don't forget to adjust the publication date."))
    status = models.IntegerField(_('status'), choices=choices.STATUS_CHOICES, default=choices.STATUS_DRAFT, db_index=True)
    opinion = models.IntegerField(_('opinion'), choices=choices.OPINION_CHOICES, blank=True)
    is_featured = models.BooleanField(_('featured'), default=False, help_text=_('Is article featured?'))
    is_reserved = models.BooleanField(_('reserved'), default=False, help_text=_('Is article reserved?'))
    content = models.TextField(_('content'))

    objects = models.Manager()
    complete = ArticleManager()
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % (self.title)
        
    def author_full_name(self):
        return self.author.get_full_name()
    author_full_name.short_description = _('author')

    @permalink
    def get_absolute_url(self):
        return ('category', (), {
            'slug': self.category.slug,
        })
        
    @permalink
    def get_archive_url(self):
        return ('archives_article', (), {
            'year': self.publication_date.strftime('%Y'),
            'month': self.publication_date.strftime('%m'),
            'day': self.publication_date.strftime('%d'),
            'slug': self.slug,
        })

    def save(self):
        self.slug = slugify(self.title)
        super(BaseArticle, self).save()


class Article(BaseArticle):
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'), null=True, blank=True, help_text=_('Please, select an illustration which will be attached to this article.')) 
    use_default_illustration = models.BooleanField(_('use default illustration'), default=False, help_text=_('Use the default category illustration to illustrate this article. If you already uploaded an illustration, it will not be used.'))
    is_illustrated = models.BooleanField(_('illustrated'), default=False, help_text=_('Is article illustrated?'))
    summary = models.TextField(_('summary'), blank=True)

    class Meta:
        db_table = 'journal_article'
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        permissions = (
            ('can_validate_illustration', 'Can validate an illustration'),
            ('can_reserve_article', 'Can reserve an article'),
            ('can_feature_article', 'Can feature an article'),
        )

    def author_full_name(self):
        return self.author.get_full_name()
    author_full_name.short_description = _('author')


class Note(BaseArticle):
    type = models.PositiveIntegerField(_('type'), choices=choices.NOTE_TYPE_CHOICES, help_text=_('Please, select a note type.'))

    class Meta:
        db_table = 'journal_note'
        verbose_name = _('note')
        verbose_name_plural = _('notes')
        permissions = (
            ('can_reserve_note', 'Can reserve a note'),
            ('can_feature_note', 'Can feature a note'),
        )

    def __unicode__(self):
        return u"%s" % (self.title)

    def bolded_type(self):
        return '<em>%s</em>' % (self.type.title,)
    bolded_type.allow_tags = True
    bolded_type.short_description = _('Type')


