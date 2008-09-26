# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.articles`` application.

"""
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from critica.apps.articles import choices
from critica.apps.articles.managers import PublishedArticleManager


class BaseArticle(models.Model):
    """
    Base article.
    
    This is an abstract class.
    
    An article is composed of::
    
        author
            * ForeignKey: django.contrib.auth.models.User
            * The article author
            * Required
            
        author_nickname
            * ForeignKey: critica.apps.users.models.UserNickname
            * The author nickname
            * Optional (can be blank)
            
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
            * ForeignKey: critica.apps.categories.models.Category
            * The article category
            * Required
            
        tags
            * TagField (from tagging)
            * The article tags
            * Optional
            
        issues
            * ManyToManyField: critica.apps.issues.models.Issue
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
            * Choices: critica.apps.article.choices.OPINION_CHOICES
            * The article opinion flag
            * Optional (can be blank)
            
        is_featured
            * BooleanField
            * Default: False
            * Is article featured?
            * Required
            
        status
            * IntegerField
            * Choices: critica.apps.articles.choices.STATUS_CHOICES
            * Default: critica.apps.articles.choices.STATUS_NEW
            * The article status
            * Required
            
        content
            * TextField
            * The article content
            * Required
            
    Indexes::
    
        * author
        * author_nickname
        * slug
        * category
        * issues
        * publication_date
        * opinion
        * is_featured
        * status
        
    Managers::
    
        objects
            Default manager: models.Manager()
            
        published
            Published articles: critica.apps.articles.managers.PublishedArticleManager()
            Note: retrieves published articles of complete issues only.

    """
    author = models.ForeignKey('auth.User', verbose_name=_('author'), help_text=_('Please, select an author for this article.'))
    author_nickname = models.ForeignKey('users.UserNickname', verbose_name=_('author nickname'), null=True, blank=True, help_text=_('If you want to sign this article under a nickname, please select one in the list. If you do not select a nickname, your signature will be your full name.'))
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    category = models.ForeignKey('categories.Category', verbose_name=_('category'), null=True, blank=True, help_text=_('Please, select a category for this article.'))
    tags = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    issues = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues.'))
    view_count = models.IntegerField(_('view count'), null=True, blank=True, editable=False)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date = models.DateField(_('publication date'), null=True, blank=True, db_index=True, help_text=_("Don't forget to adjust the publication date."))
    opinion = models.IntegerField(_('opinion'), choices=choices.OPINION_CHOICES, null=True, blank=True, db_index=True)
    is_featured = models.BooleanField(_('featured'), default=False, db_index=True, help_text=_('Is featured?'))
    is_ready_to_publish = models.BooleanField(_('ready to publish'), default=False, db_index=True, help_text=_('Is ready to be publish?'))
    is_reserved = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is reserved?'))
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
    
    def save(self):
        """ 
        Object pre-saving operations:
        
        * Generates slug from title
        * Save article
        
        """
        self.slug = slugify(self.title)
        super(BaseArticle, self).save()


class Article(BaseArticle):
    """
    Article.
    
    Database table name: ``articles_article``.
    
    An article is composed of::
    
        Inherits from BaseArticle.
        So, all fields of this abstract class and fields below.
        
        illustration
            * ForeignKey: critica.apps.illustrations.models.Illustration
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
    illustration = models.ForeignKey('illustrations.Illustration', verbose_name=_('illustration'), null=True, blank=True, help_text=_('Please, select an illustration which will be attached to this article.')) 
    use_default_illustration = models.BooleanField(_('use default illustration'), default=False, db_index=True, help_text=_('Use the default category illustration to illustrate this article. If you already uploaded an illustration, it will not be used.'))
    summary = models.TextField(_('summary'))

    class Meta:
        db_table = 'articles_article'
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        permissions = (
            ('can_feature_article', 'Can feature an article'),
            ('can_reserve_article', 'Can reserve an article'),
            ('can_publish_article', 'Can publish an article'),
        )

