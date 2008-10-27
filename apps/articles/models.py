# -*- coding: utf-8 -*-
"""
Models of ``critica.apps.articles`` application.

"""
import datetime
from tagging.fields import TagField

from django.db import models
from django.db.models import permalink
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from critica.apps.articles import choices
from critica.apps.articles.managers import PublishedArticleManager


def get_image_path(instance, filename):
    """
    Dynamic image upload path.
    
    """
    return 'upload/images/visuels/%s/%s-%s' % (instance.category.slug, instance.id, filename)

        
class BaseArticle(models.Model):
    """
    Base article.
    
    This is an abstract class.
    
    Fields::
    
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
            
        is_ready_to_publish
            * BooleanField
            * Default: False
            * Is article ready to publish?
            * Required
            
        is_reserved
            * BooleanField
            * Default: False
            * Is article reserved?
            * Required
            
        summary
            * TextField
            * The article summary
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
        * is_ready_to_publish
        * is_reserved

    """
    author               = models.ForeignKey('auth.User', verbose_name=_('author'), help_text=_('Please, select an author for this article.'))
    author_nickname      = models.ForeignKey('users.UserNickname', verbose_name=_('author nickname'), null=True, blank=True, help_text=_('If you want to sign this article under a nickname, please select one in the list. If you do not select a nickname, your signature will be your full name.'))
    title                = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('255 characters max.'))
    slug                 = models.SlugField(_('slug'), max_length=255, blank=True, editable=False)
    category             = models.ForeignKey('categories.Category', verbose_name=_('category'), null=True, blank=True, help_text=_('Please, select a category for this article.'))
    tags                 = TagField(help_text=_('Please, enter tags separated by commas or spaces.'))
    issues               = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues.'))
    view_count           = models.IntegerField(_('view count'), null=True, blank=True, editable=False)
    creation_date        = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date    = models.DateTimeField(_('modification date'), auto_now_add=True, editable=False)
    publication_date     = models.DateField(_('publication date'), null=True, blank=True, db_index=True, help_text=_("Don't forget to adjust the publication date."))
    opinion              = models.IntegerField(_('opinion'), choices=choices.OPINION_CHOICES, null=True, blank=True, db_index=True)
    image                = models.ImageField(upload_to=get_image_path, verbose_name=_('image'), blank=True, help_text=_('Please, select an image which will be attached to this article.')) 
    image_legend         = models.CharField(_('legend'), max_length=255, blank=True)
    image_credits        = models.CharField(_('credits'), max_length=255, blank=True, default='Critic@') 
    is_featured          = models.BooleanField(_('featured'), default=False, db_index=True, help_text=_('Is featured?'))
    is_ready_to_publish  = models.BooleanField(_('ready to publish'), default=False, db_index=True, help_text=_('Is ready to be publish?'))
    is_reserved          = models.BooleanField(_('reserved'), default=False, db_index=True, help_text=_('Is reserved?'))
    summary              = models.TextField(_('summary'))
    content              = models.TextField(_('content'))
    
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


    @permalink
    def get_absolute_url(self):
        """
        Returns absolute URL.
        
        """
        return ('category', (), {'category_slug': self.category.slug})

    
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
    
    Fields::
    
        See BaseArticle.
            
    Managers::
    
        objects
            Default manager.
            Manager: models.Manager()
        
        published
            Only returns ready to publish articles.
            Manager: critica.apps.articles.managers.PublishedArticleManager()
            
    Indexes::
    
        See BaseArticle.
            
    """
    objects   = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        """ 
        Model metadata. 
        
        """
        db_table = 'articles_article'
        verbose_name = _('article')
        verbose_name_plural = _('articles')


