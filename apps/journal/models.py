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
from critica.apps.journal.managers import PositionManager
from critica.apps.journal.managers import IllustrationManager
from critica.apps.journal.managers import ReportageManager
from critica.apps.journal.managers import ArticleManager
from critica.apps.journal.managers import IssueManager
from critica.apps.journal.managers import PageManager


class Category(models.Model):
    """
    Journal category.
    
    A journal category is composed of::
    
        name
            The category name. Max. 20 characters.
            Required.
            
        slug
            The category slug. Max. 40 characters. Must be unique.
            
    Managers::
        
        objects
            All objects.
            
    Properties::
    
        complete_article_set
            Returns complete article set.
    
    """
    name = models.CharField(_('name'), max_length=20, help_text=_('As short as possible. 20 characters max.'))
    slug = models.SlugField(_('slug'), max_length=40, null=True, blank=True, unique=True, editable=False)
    
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
        return ('journal_category', (), { 
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


class Position(models.Model):
    """
    Article position in the page.
    
    A position is composed of::
    
        position
            Position in the page. Must be unique.
            Required.
            
        description
            Short description of the position. Max. 100 characters.
            Required.
            
    Managers::
    
        objects
            All objects.

    """
    position = models.PositiveIntegerField(_('position'), unique=True, help_text=_('Hierarchical position in the page.'))
    description = models.CharField(_('description'), max_length=100, help_text=_('A short description of this position'))
    
    class Meta:
        """ Model metadata. """
        verbose_name = _('position')
        verbose_name_plural = _('positions')
    
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.position
        
    # Managers
    objects = PositionManager()


class Illustration(models.Model):
    """
    Article illustration.
    
    An article illustration is composed of::
    
        image
            The image file path.
            Required.
            
        creation_date
            The image creation date.
            
        modification_date
            The image modification date.
            
        credits
            The image credits.
            Required.
            
        legend
            The image legend.
            Required.
            
        is_generic
            Is image a generic image? Default to ``False``.
            Required.
    
    Managers::
    
        objects
            All objects.
    
    """
    image = models.ImageField(upload_to='critica/upload/%Y/%m/%d', max_length=200, help_text=_('Please, select an image to upload'))
    category = models.ForeignKey(Category, verbose_name=_('category'), null=True, blank=True)
    creation_date = models.DateTimeField(_('creation date'), null=True, blank=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), null=True, blank=True, editable=False)
    credits = models.CharField(_('credits'), max_length=100, default=_('all rights reserved'), help_text=_('100 characters max.'))
    legend = models.CharField(_('legend'), max_length=100, blank=True, help_text=_('100 characters max.'))
    is_generic = models.BooleanField(_('generic'), default=False, db_index=True, help_text=_('Could image be generic?'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('illustration')
        verbose_name_plural = _('illustrations')
        
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.legend
    
    def thumbnail(self):
        return '<img src="%s%s" alt="%s" height="60" />' % (settings.MEDIA_URL, self.image, self.legend)
    thumbnail.allow_tags = True
    thumbnail.short_description = _('Illustration')
    
    def bolded_category(self):
        return '<strong>%s</strong>' % (self.category,)
    bolded_category.allow_tags = True
    bolded_category.short_description = _('Category')
    
    def save(self):
        """ Object pre-saving operations. """
        if not self.id:
            self.creation_date = datetime.now()
            self.modification_date = self.creation_date
        else:
            self.modification_date = datetime.now()
        super(Illustration, self).save()
        
    # Managers
    objects = IllustrationManager()


class Reportage(models.Model):
    """
    A video reportage.
    
    """
    video_name = models.CharField(_('video name'), max_length=255, help_text=_('Please, enter a name for this video.'))
    video_link = models.CharField(_('video link'), max_length=255, help_text=_('Please, enter the video URL.'))
    creation_date = models.DateTimeField(_('creation date'), null=True, blank=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), null=True, blank=True, editable=False)
    is_published = models.BooleanField(_('published'), default=False, help_text=_('Is video ready to be published?'))
    
    class Meta:
        """ Model metadata. """
        verbose_name = _('reportage')
        verbose_name_plural = _('reportages')
        
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.video_name

    def save(self):
        """ Object pre-saving operations. """
        if not self.id:
            self.creation_date = datetime.now()
            self.modification_date = self.creation_date
        else:
            self.modification_date = datetime.now()
        super(Reportage, self).save() 

    # Managers
    objects = models.Manager()
    published = ReportageManager()


class Type(models.Model):
    """
    Journal article type (surtitre).
    
    A type is composed of::
    
        name
            The type name.
            
    """
    name = models.CharField(_('name'), max_length=50)

    class Meta:
        verbose_name = _('type')
        verbose_name_plural = _('types')

    def __unicode__(self):
        return u'%s' % self.name


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
    publication_date = models.DateTimeField(_('publication date'), null=True, blank=True, help_text=_("Don't forget to adjust the publication date"))
    is_complete = models.BooleanField(_('complete'), default=False, db_index=True, help_text=_('Is issue complete'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('issue')
        verbose_name_plural = _('issues')
        
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.number
        
    @permalink
    def get_absolute_url(self):
        """ Returns issue's absolute URL. """
        return ('issue', (), { 
            'issue': self.number,
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
        if not self.publication_date:
            self.publication_date = datetime.now()
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
        
        issue
            The article issue.
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
    slug = models.SlugField(_('slug'), max_length=255, blank=True, null=True)
    
    author = models.ForeignKey(User, verbose_name=_('author'), db_index=True, help_text=_('Please, select an author for this article.'))
    issue = models.ForeignKey(Issue, verbose_name=_('issue'), db_index=True, help_text=_('Please, select an issue.'))
    category = models.ForeignKey(Category, verbose_name=_('category'), db_index=True, help_text=_('Please, select a category for this article.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    position = models.ForeignKey(Position, verbose_name=_('position'), null=True, blank=True, help_text=_('Please, select a position for this article.'))
    
    creation_date = models.DateTimeField(_('creation date'), null=True, blank=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), null=True, blank=True, editable=False)
    publication_date = models.DateTimeField(_('publication date'), null=True, blank=True, help_text=_("Don't forget to adjust the publication date."))
    
    citation = models.TextField(_('citation'), null=True, blank=True, help_text=_('Enter a citation which will be attached to this article.'))
    illustration = models.ForeignKey(Illustration, verbose_name=_('illustration'), null=True, blank=True, help_text=_('Please, select an illustration which will be attached to this article.'))
    
    is_reserved = models.BooleanField(_('reserved'), default=False, help_text=_('Is article reserved?'))
    is_featured = models.BooleanField(_('featured'), default=False, help_text=_('Is article featured?'))
    is_published = models.BooleanField(_('published'), default=False, help_text=_('Is article published?'))
    is_illustrated = models.BooleanField(_('illustrated'), default=False, help_text=_('Is article illustrated?'))
    
    summary = models.TextField(_('summary'))
    content = models.TextField(_('content'))
    
    related_articles = models.ManyToManyField('self', verbose_name=('related articles'), null=True, blank=True, help_text=_('You can select some related articles to attach to this one.'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __unicode__(self):
        """ Object human-readable string representation. """
        return u"%s: %s" % (self.issue, self.title)
        
    @permalink
    def get_absolute_url(self):
        """ Returns article's absolute URL. """
        return ('article', (), { 
            'issue': self.issue,
            'category': self.category,
            'article': self.slug,
        })
    
    def save(self):
        """ Object pre-saving operations. """
        if not self.id:
            self.creation_date = datetime.now()
            self.modification_date = self.creation_date
            self.publication_date = self.creation_date
        else:
            self.modification_date = datetime.now()
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
    creation_date = models.DateTimeField(_('creation date'), null=True, blank=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), null=True, blank=True, editable=False)
    is_complete = models.BooleanField(_('complete'), default=False, help_text=_('Is page complete?'))

    class Meta:
        """ Model metadata. """
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.category

    def save(self):
        """ Object pre-saving operations. """
        if not self.id:
            self.creation_date = datetime.now()
            self.modification_date = self.creation_date
        else:
            self.modification_date = datetime.now()
        super(Page, self).save()
        
    # Managers
    objects = models.Manager()
    complete = PageManager()

