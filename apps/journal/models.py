# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.journal``.

"""
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.models import Tag
from tagging.fields import TagField
from critica.apps.journal.managers import CategoryManager
from critica.apps.journal.managers import IllustrationManager
from critica.apps.journal.managers import ReportageManager
from critica.apps.journal.managers import TypeManager
from critica.apps.journal.managers import ArticleManager
from critica.apps.journal.managers import IssueManager
from critica.apps.journal.managers import PageManager


class Category(models.Model):
    """
    Journal category.

    A journal category is composed of::

        name
            The category name.
            Required.

        slug
            The category slug.

        description
            The category description.

    Managers::

        objects
            All objects.

    Properties::

        complete_article_set
            Returns complete article set.

    """
    name = models.CharField(_('name'), max_length=255, help_text=_('As short as possible.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, unique=True, editable=False)
    description = models.CharField(_('description'), max_length=255, blank=True, help_text=_('A short description of the category. It will not be displayed on the website.'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        """ Returns category's absolute URL. """
        return ('category', (), {
            'category': self.slug,
        })

    def _get_complete_articles(self):
        """
        Returns complete article set.
        Access this through the property ``complete_article_set``.

        """
        return self.article_set.filter(is_published=True, is_illustrated=True, is_reserved=False)
    complete_article_set = property(_get_complete_articles)

    def save(self):
        """ Object pre-saving operations. """
        self.slug = slugify(self.name)
        super(Category, self).save()

    # Managers
    objects = CategoryManager()


class Illustration(models.Model):
    """
    Article illustration.

    An article illustration is composed of::

        image
            The image file path.
            Required.

        category
            The image category.

        creation_date
            The image creation date.

        modification_date
            The image modification date.

        credits
            The image credits. Default to ``all rights reserved``.
            Required.

        legend
            The image legend.

        is_generic
            Is image a generic image? Default to ``False``.
            Required.

    Managers::

        objects
            All objects.

    """
    image = models.ImageField(upload_to='critica/upload/%Y/%m/%d', max_length=200, help_text=_('Please, select an image to upload'))
    category = models.ForeignKey(Category, verbose_name=_('category'), null=True, blank=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend = models.CharField(_('legend'), max_length=100, blank=True, help_text=_('100 characters max.'))
    is_generic = models.BooleanField(_('generic'), default=False, db_index=True, help_text=_('Could image be generic?'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('illustration')
        verbose_name_plural = _('illustrations')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.image

    def thumbnail(self):
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.legend)
    thumbnail.allow_tags = True
    thumbnail.short_description = _('Illustration')

    def bolded_category(self):
        return '<strong>%s</strong>' % (self.category,)
    bolded_category.allow_tags = True
    bolded_category.short_description = _('Category')

    # Managers
    objects = IllustrationManager()


class Reportage(models.Model):
    """
    Video reportage.

    A video reportage is composed of::

        video_name
            The video name (identifier).
            Required.

        video_link
            The video link.
            Required.

        creation_date
            The video creation date.

        modification_date
            The video modification date.

        is_published
            Is the video ready to be published? Default to ``False``.

    Managers::

        objects
            All objects.

        published
            All reportages ready to be published.

    """
    video_name = models.CharField(_('video name'), max_length=255, help_text=_('Please, enter a name for this video.'))
    video_link = models.CharField(_('video link'), max_length=255, help_text=_('Please, enter the video URL.'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    is_published = models.BooleanField(_('published'), default=False, help_text=_('Is video ready to be published?'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('reportage')
        verbose_name_plural = _('reportages')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.video_name

    # Managers
    objects = models.Manager()
    published = ReportageManager()


class Type(models.Model):
    """
    Journal article type (surtitre).

    A type is composed of::

        title
            The type title. Displayed on the website.

        description
            The type description. Not displayed on the website.

    Managers::

        objects
            All objects.

    """
    title = models.CharField(_('title'), max_length=100, help_text=_('Please, enter the type title. It will be displayed on the website.'))
    description = models.CharField(_('description'), max_length=255, help_text=_('Please, enter the type description. It will not be displayed on the website.'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('type')
        verbose_name_plural = _('types')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.description

    # Managers
    objects = TypeManager()


class Issue(models.Model):
    """
    Journal issue.

    An issue is composed of::

        number
            The issue number. Must be unique.

        publication_date
            The issue publication date.

        is_complete
            Is issue complete? Default to ``False``.

    Managers::

        objects
            All objects.

    Properties::

        complete_article_set
            Returns complete article set.

    """
    number = models.PositiveIntegerField(_('number'), unique=True, help_text=_("Please, enter the issue's number."))
    publication_date = models.DateTimeField(_('publication date'), blank=True, help_text=_("Don't forget to adjust the publication date"))
    is_complete = models.BooleanField(_('complete'), default=False, db_index=True, help_text=_('Is issue complete'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('issue')
        verbose_name_plural = _('issues')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.number

    def _get_complete_articles(self):
        """
        Returns complete article set.
        Access this through the property ``complete_article_set``.

        """
        return self.article_set.filter(is_published=True, is_illustrated=True, is_reserved=False)
    complete_article_set = property(_get_complete_articles)

    def save(self):
        """ Object pre-saving operations. """
        super(Issue, self).save()
        # creates pages for this issue
        categories = Category.objects.all()
        for category in categories:
            page = Page(issue=self, category=category)
            page.save()

    # Managers
    objects = models.Manager()
    complete = IssueManager()


class Article(models.Model):
    """
    Journal article.

    An article is composed of::

        type
            The article type or surtitre (from ``Type``).
            Required.

        title
            The article title.
            Required.

        slug
            The article slug.

        author
            The article author.
            Required.

        issues
            The article issues.
            Required.

        category
            The article category (from ``Category``)
            Required.

        tags
            The article tags (from ``Tag``, ``tagging`` application).

        position
            The article position in the page (from ``Position``).

        creation_date
            The article creation date.

        modification_date
            The article modification date.

        publication_date
            The article publication date.

        citation
            The article citation.

        illustration
            The article illustration (from ``Illustration``).

        is_featured
            Is article featured? Default to ``False``.

        is_published
            Is article ready to publish? Default to ``False``.

        is_illustrated
            Is article illustrated? Default to ``False``.

        summary
            The article summary.
            Required.

        content
            The article content. Required.
            Required.

    Managers::

        object
            All objects.

        complete
            Complete articles.

    """
    type = models.ForeignKey(Type, verbose_name=_('type'), help_text=_('Please, select the article type.'))
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True)

    author = models.ForeignKey(User, verbose_name=_('author'), help_text=_('Please, select an author for this article.'))
    issues = models.ManyToManyField(Issue, verbose_name=_('issues'), help_text=_('Please, select one or several issues.'))
    category = models.ForeignKey(Category, verbose_name=_('category'), help_text=_('Please, select a category for this article.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    viewed_count = models.PositiveIntegerField(_('viewed count'), null=True, blank=True, editable=False)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date = models.DateTimeField(_('publication date'), blank=True, help_text=_("Don't forget to adjust the publication date."))

    citation = models.TextField(_('citation'), blank=True, help_text=_('Enter a citation which will be attached to this article.'))
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'), null=True, blank=True, help_text=_('Please, select an illustration which will be attached to this article.'))

    is_reserved = models.BooleanField(_('reserved'), default=False, help_text=_('Is article reserved?'))
    is_featured = models.BooleanField(_('featured'), default=False, help_text=_('Is article featured?'))
    is_published = models.BooleanField(_('published'), default=False, help_text=_('Is article published?'))
    is_illustrated = models.BooleanField(_('illustrated'), default=False, help_text=_('Is article illustrated?'))

    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'))

    related_articles = models.ManyToManyField('self', verbose_name=('related articles'), null=True, blank=True, help_text=_('You can select some related articles to attach to this one.'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u"%s: %s" % (self.category, self.title)

    @permalink
    def get_absolute_url(self):
        """ Returns article's absolute URL. """
        return ('category', (), {
            'category': self.category.slug,
        })
        
    @permalink
    def get_archive_url(self):
        """ Returns article's archive URL. """
        return ('archives_article', (), {
            'year': self.publication_date.strftime('%Y'),
            'month': self.publication_date.strftime('%m'),
            'day': self.publication_date.strftime('%d'),
            'slug': self.slug,
        })

    def bolded_type(self):
        """ Returns bolded type title for admin list display. """
        return '<em>%s</em>' % (self.type.title,)
    bolded_type.allow_tags = True
    bolded_type.short_description = _('Type')

    def author_full_name(self):
        """ Returns author's full name for admin list display. """
        return self.author.get_full_name()
    author_full_name.short_description = _('author')

    def save(self):
        """ Object pre-saving operations. """
        self.slug = slugify(self.title)
        super(Article, self).save()


    # Managers
    objects = models.Manager()
    complete = ArticleManager()


class Page(models.Model):
    """
    Journal page.

    A journal page is composed of::

        issue
            The page issue.

        category
            The page category.

        articles
            The page articles.

        illustration
            The page illustration.

        reportage
            The page reportage.

        creation_date
            The page creation date.

        modification_date
            The page modification date.

        is_complete
            Is page complete? Default to ``False``.

    Managers::

        objects
            All objects.

        complete
            Complete pages.

    """
    issue = models.ForeignKey(Issue, verbose_name=_('issue'), help_text=_('Please, select an issue.'))
    category = models.ForeignKey(Category, verbose_name=_('category'), help_text=_('Please, select a category.'))
    articles = models.ManyToManyField(Article, verbose_name=_('articles'), null=True, blank=True, help_text=_('Please, select articles to insert in this page.'))
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'), null=True, blank=True, help_text=_('Optional'))
    reportage = models.ForeignKey(Reportage, verbose_name=_('reportage'), null=True, blank=True, help_text=_('Optional'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    is_complete = models.BooleanField(_('complete'), default=False, help_text=_('Is page complete?'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.category

    # Managers
    objects = models.Manager()
    complete = PageManager()


