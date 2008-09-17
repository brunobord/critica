# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.journal`` application.

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
from critica.apps.journal.managers import PublishedArticleManager
from critica.apps.journal.managers import CompleteIssueManager
from critica.apps.journal.managers import PublishedIssueManager


class Category(models.Model):
    """
    Category.
    
    Database table name: ``journal_category``.
    
    A category is composed of::
    
        name
            * CharField
            * 255 characters max.
            * The category name
            * Required
            
        slug
            * SlugField
            * 255 characters max.
            * The category slug (URL)
            * Must be unique
            * No editable
            * Required
            
        description
            * CharField
            * 255 characters max.
            * The category description
            * Optional (can be blank)
            
        image
            * ImageField (media/upload/categories/)
            * The default category illustration
            * 200 characters max.
            * Required
            
        image_credits
            * CharField
            * 100 characters max.
            * The default category illustration credits
            * default value: all rights reserved
            * Required
            
        image_legend
            * CharField
            * 100 characters max.
            * The default category illustration legend
            * Required
            
        position_on_page
            * IntegerField
            * The category position on the cover
            * choices: critica.apps.journal.choices.CATEGORY_POSITION_CHOICES
            * Required
            
        creation_date
            * DateTimeField
            * The category creation date
            * auto_now_add
            * No editable
            * Required
            
        modification_date
            * DateTimeField
            * The category modification date
            * auto_now
            * No editable
            * Required

    Indexes::
    
        * slug
        * position_on_page

    Managers::
    
        objects
            Default manager: models.Manager()
    
    Properties::
    
        published_article_set
            Retrieves category published articles
    
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('As short as possible.'))
    slug = models.SlugField(_('URL'), max_length=255, blank=True, unique=True, editable=False)
    description = models.CharField(_('description'), max_length=255, blank=True, help_text=_('A short description of the category. It will not be displayed on the website.'))
    image = models.ImageField(upload_to='upload/categories/', max_length=200, help_text=_('Please, upload an image for this category (it will be used as default category illustration).'))
    image_credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    image_legend = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    position_on_page = models.IntegerField(_('position'), choices=choices.CATEGORY_POSITION_CHOICES, db_index=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name

    def slug_ld(self):
        """ 
        Formatted slug for admin list_display option. 
        
        """
        return 'http://www.critica.fr/<strong>%s</strong>/' % (self.slug)
    slug_ld.allow_tags = True
    slug_ld.short_description = _('URL')
    
    def image_ld(self):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.image_legend)
    image_ld.allow_tags = True
    image_ld.short_description = _('Default illustration')

    @permalink
    def get_absolute_url(self):
        """ 
        Returns the category absolute URL. 
        
        """
        return ('category', (), {'slug': self.slug})
        
    def get_rss_url(self):
        """ 
        Returns the category RSS feed URL. 
        
        """
        return u'/rss/rubriques/%s/' % self.slug

    def _get_published_article_set(self):
        """
        Returns published article set.
        Access this through the property ``published_article_set``. 
        
        """
        return self.article_set.filter(
            issues__is_complete=True, 
            issues__is_published=True, 
            is_published=True, 
            is_reserved=False
        )
    published_article_set = property(_get_published_article_set)
    
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from title
        * Save category
        
        """
        self.slug = slugify(self.name)
        super(Category, self).save()


# ------------------------------------------------------------------------------


class NoteType(models.Model):
    """
    Note type.
    
    Database table name: ``journal_note_type``.
    
    A note type is composed of::
    
        name
            * CharField
            * 255 characters max.
            * Required
            
        position_on_page
            * IntegerField
            * choices: critica.apps.journal.choices.TYPE_POSITION_CHOICES
            * Required
            
    Indexes::
    
        * position_on_page
        
    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    name = models.CharField(_('name'), max_length=255)
    position_on_page = models.IntegerField(_('position'), choices=choices.TYPE_POSITION_CHOICES, db_index=True)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('note type')
        verbose_name_plural = _('note types')
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.name


# ------------------------------------------------------------------------------


class Illustration(models.Model):
    """
    Illustration.
    
    Database table name: ``journal_illustration``.
    
    An illustration is composed of::
    
        submitter
            * ForeignKey(auth.User)
            * User who submitted the illustration
            * Required
            
        category
            * ForeignKey(Category)
            * The illustration category
            * Required
            
        image
            * ImageField (media/critica/upload/%Y/%m/%d)
            * 200 characters max.
            * The illustration image file
            * Required
            
        credits
            * CharField
            * 100 characters max.
            * The illustration credits
            * Default value: all rights reserved
            * Required
            
        legend
            * CharField
            * 100 characters max.
            * The illustration legend
            * Required
            
        creation_date
            * DateTimeField
            * auto_now_add
            * The illustration creation date
            * No editable
            * Required
        
        modification_date
            * DateTimeField
            * auto_now
            * No editable
            * Required
    
    Indexes::
    
        * submitter
        * category

    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    category = models.ForeignKey(Category, verbose_name=_('category'), blank=True)
    image = models.ImageField(upload_to='critica/upload/%Y/%m/%d', max_length=200, help_text=_('Please, select an image to upload'))
    credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend = models.CharField(_('legend'), max_length=100, help_text=_('100 characters max.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('illustration')
        verbose_name_plural = _('illustrations')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.image

    def image_ld(self):
        """ 
        Image thumbnail for admin list_display option. 
        
        """
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.legend)
    image_ld.allow_tags = True
    image_ld.short_description = _('Illustration')

    def category_ld(self):
        """
        Formatted category for admin list_display option.
        
        """
        return '<strong>%s</strong>' % (self.category,)
    category_ld.allow_tags = True
    category_ld.short_description = _('Category')


# ------------------------------------------------------------------------------


class Reportage(models.Model):
    """
    Reportage.
    
    Database table name: ``journal_reportage``.
    
    A reportage is composed of::
    
        submitter
            * ForeignKey(auth.User)
            * User who submitted the reportage
            * Required
            
        video_name
            * CharField
            * 255 characters max.
            * The video name
            * Required
            
        video_link
            * CharField
            * 255 characters max.
            * The video link
            * Required
            
        creation_date
            * DateTimeField
            * auto_now_add
            * Reportage creation date
            * No editable
            * Required
            
        modification_date
            * DateTimeField
            * auto_now
            * Reportage modification date
            * No editable
            * Required
            
        is_published
            * BooleanField
            * Default: False
            * Required
    
    Indexes::
    
        * submitter
        * is_published
    
    Managers::
    
        objects
            Default manager: models.Manager()
    
    """
    submitter = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    video_name = models.CharField(_('video name'), max_length=255, help_text=_('Please, enter a name for this video.'))
    video_link = models.CharField(_('video link'), max_length=255, help_text=_('Please, enter the video URL.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    is_published = models.BooleanField(_('published'), default=False, db_index=True, help_text=_('Is video ready to be published?'))
    
    objects = models.Manager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name = _('reportage')
        verbose_name_plural = _('reportages')

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.video_name


# ------------------------------------------------------------------------------


class Issue(models.Model):
    """
    Issue.
    
    Database table name: ``journal_issue``.
    
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
            
        is_complete
            * BooleanField
            * Default: False
            * If issue complete?
            * Required
            
        is_published
            * BooleanField
            * Default: False
            * If issue ready to be published?
            * Required
    
    Indexes::
    
        * number
        * is_complete
        * is_published
    
    Managers::
    
        objects
            Default manager: models.Manager()
        
        complete
            Complete issues: critica.apps.journal.managers.CompleteIssueManager()
            To retrieve complete published issues: Issue.complete.published
            
        published
            Published issues: critica.apps.journal.managers.PublishedIssueManager()
            To retrieve complete published issues: Issue.published.complete
    
    Properties::
    
        published_article_set
            Returns issue's published article.
    
    """
    number = models.PositiveIntegerField(_('number'), unique=True, help_text=_("Please, enter the issue's number."))
    publication_date = models.DateField(_('publication date'), blank=True, help_text=_("Don't forget to adjust the publication date"))
    is_complete = models.BooleanField(_('complete'), default=False, db_index=True, help_text=_('Is issue complete'))
    is_published = models.BooleanField(_('published'), default=False, db_index=True, help_text=_('Is issue ready to be published?'))
    
    objects = models.Manager()
    complete = CompleteIssueManager()
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

    def _get_published_article_set(self):
        """
        Returns published article set.
        Access this through the property ``published_article_set``. 
        
        """
        return self.article_set.filter(is_published=True, is_reserved=False)
    published_article_set = property(_get_published_article_set)


# ------------------------------------------------------------------------------


class BaseArticle(models.Model):
    """
    Base article.
    
    This is an abstract class.
    
    An article is composed of::
    
        author
            * ForeignKey(auth.User)
            * The article author
            * Required
            
        title
            * CharField
            * 255 characters max.
            * The article title
            * Required
            
        slug
            * SlugField
            * 255 characters max.
            * The article slug
            * No editable
            * Optional (can be blank)
            
        category
            * ForeignKey(Category)
            * The article category
            * Required
            
        tags
            * TagField (from tagging)
            * The article tags
            * Optional
            
        issues
            * ManyToManyField(Issue)
            * The article issues
            * Optional (can be blank)
            
        view_count
            * PositiveIntegerField
            * The article view count
            * No editable
            * Optional (can be blank)
            
        creation_date
            * DateTimeField
            * auto_now_add
            * The article creation date
            * Required
            
        modification_date
            * DateTimeField
            * auto_now
            * The article modification date
            * Required
            
        publication_date
            * DateField
            * The article publication date
            * Optional (can be blank)
        
        opinion
            * IntegerField
            * Choices: critica.apps.journal.choices.OPINION_CHOICES
            * The article opinion flag
            * Optional (can be blank)
            
        is_featured
            * BooleanField
            * Default: False
            * Is article featured?
            * Required
            
        is_reserved
            * BooleanField
            * Default: False
            * Is article reserved?
            * Required
            
        is_published
            * BooleanField
            * Default: False
            * Is article ready to be published?
            * Required
            
        content
            * TextField
            * The article content
            * Required
            
    Indexes::
    
        * author
        * slug
        * category
        * issues
        * publication_date
        * opinion
        * is_featured
        * is_reserved
        * is_published
        
    Managers::
    
        objects
            Default manager: models.Manager()
            
        published
            Published articles: critica.apps.journal.managers.PublishedArticleManager()
            Note: retrieves published articles of complete and published issues only.

    """
    author = models.ForeignKey('auth.User', verbose_name=_('author'), help_text=_('Please, select an author for this article.'))
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    category = models.ForeignKey(Category, verbose_name=_('category'), help_text=_('Please, select a category for this article.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    issues = models.ManyToManyField(Issue, verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues.'))
    view_count = models.PositiveIntegerField(_('view count'), blank=True, editable=False)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date = models.DateField(_('publication date'), blank=True, db_index=True, help_text=_("Don't forget to adjust the publication date."))
    opinion = models.IntegerField(_('opinion'), choices=choices.OPINION_CHOICES, blank=True, db_index=True)
    is_featured = models.BooleanField(_('featured'), default=False, db_index=True, help_text=_('Is article featured?'))
    is_reserved = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is article reserved?'))
    is_published = models.BooleanField(_('published'), default=False, db_index=True, help_text=_('Is article ready to be published?'))
    content = models.TextField(_('content'))

    objects = models.Manager()
    published = PublishedArticleManager()
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        abstract = True

    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u"%s" % (self.title)
        
    def author_ld(self):
        """
        Formatted author for admin list_display option.
        
        """
        return self.author.get_full_name()
    author_ld.short_description = _('author')

    @permalink
    def get_absolute_url(self):
        """ 
        Returns the article absolute URL. 
        
        """
        return ('category', (), {'slug': self.category.slug})
        
    @permalink
    def get_archive_url(self):
        """ 
        Returns the article archive absolute URL. 
        
        """
        return ('archives_article', (), {
            'year': self.publication_date.strftime('%Y'),
            'month': self.publication_date.strftime('%m'),
            'day': self.publication_date.strftime('%d'),
            'slug': self.slug,
        })

    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from title
        * Save article
        
        """
        self.slug = slugify(self.title)
        super(BaseArticle, self).save()


# ------------------------------------------------------------------------------


class Article(BaseArticle):
    """
    Article.
    
    Database table name: ``journal_article``.
    
    An article is composed of::
    
        Inherits from BaseArticle.
        So, all fields of this abstract class and fields below.
        
        illustration
            * ForeignKey(Illustration)
            * The article illustration
            * Optional (can be blank)
            
        use_default_illustration
            * BooleanField
            * Default: False
            * Use the default category illustration?
            * Required
            
        is_illustrated
            * BooleanField
            * Default: False
            * Is article illustrated?
            * Required
            
        summary
            * TextField
            * The article summary
            * Required
            
    Indexes::
    
        BaseArticle indexes and below.
        
        * use_default_illustration
        * is_illustrated
            
    Managers::
    
        See BaseArticle.
        
    Permissions::
    
        can_validate_illustration
            Can validate an illustration
            
        can_reserve_article
            Can reserve an article
            
        can_feature_article
            Can feature an article
    
    
    """
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'), blank=True, help_text=_('Please, select an illustration which will be attached to this article.')) 
    use_default_illustration = models.BooleanField(_('use default illustration'), default=False, db_index=True, help_text=_('Use the default category illustration to illustrate this article. If you already uploaded an illustration, it will not be used.'))
    is_illustrated = models.BooleanField(_('illustrated'), default=False, db_index=True, help_text=_('Is article illustrated?'))
    summary = models.TextField(_('summary'))

    class Meta:
        db_table = 'journal_article'
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        permissions = (
            ('can_validate_illustration', 'Can validate an illustration'),
            ('can_reserve_article', 'Can reserve an article'),
            ('can_feature_article', 'Can feature an article'),
        )


# ------------------------------------------------------------------------------


class Note(BaseArticle):
    """
    Note.
    
    Database table name: ``journal_note``.
    
    A note is composed of::
    
        Inherits from BaseArticle.
        So, all fields of this abstract class and fields below.
    
        type
            * ForeignKey(Type)
            * The note type
            * Required

    Indexes::
    
        BaseArticle indexes and below.
        
        * type
            
    Managers::
    
        See BaseArticle.
        
    Permissions::
            
        can_reserve_note
            Can reserve a note
            
        can_feature_note
            Can feature a note
    
    """
    type = models.ForeignKey(NoteType, verbose_name=_('type'), help_text=_('Please, select a note type.'))

    class Meta:
        db_table = 'journal_note'
        verbose_name = _('note')
        verbose_name_plural = _('notes')
        permissions = (
            ('can_reserve_note', 'Can reserve a note'),
            ('can_feature_note', 'Can feature a note'),
        )

    def type_ld(self):
        """
        Formatted type for admin list_display option.
        
        """
        return '<em>%s</em>' % (self.type.title,)
    type_ld.allow_tags = True
    type_ld.short_description = _('Type')


