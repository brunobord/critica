# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.newsletter``.

"""
import hashlib
from django.db import models
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import Article
from critica.apps.categories.models import Category


class Newsletter(models.Model):
    """
    Newsletter.
    
    A newsletter is composed of::
    
        sending_date
            The newsletter is sent at this date.
            
        recipient_count
            How many recipients received the newsletter.
            
        viewed_count
            How many times the newsletter has been viewed.
            
        hash_code
            Automatically generated using ``sending_date``.
            
        is_published
            Ready to send to subscribers.
            
        sending_start_date
            Sending starts at this date.
        
        sending_end_date
            Sending ends at this date.
             
    """
    sending_date       = models.DateTimeField(_('sending date'), null=True, blank=True, help_text=_('The newsletter is sent at this date.'))
    recipient_count    = models.PositiveIntegerField(_('recipient count'), default=0, editable=False)
    viewed_count       = models.PositiveIntegerField(_('viewed count'), default=0, editable=False)
    hash_code          = models.CharField(_('hash code'), max_length=32, default="x", db_index=True, editable=False)
    is_published       = models.BooleanField(_('published'), default=False)
    sending_start_date = models.DateTimeField(_('sending start at'), null=True, blank=True)
    sending_end_date   = models.DateTimeField(_('sending end at'), null=True, blank=True)

    class Meta:
        """ Model metadata. """
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')
        
    def __unicode__(self):
        """ Object human-readable string representation. """
        return u'%s' % self.sending_date
        
    def save(self):
        """ Object pre-saving operations. """
        hash = hashlib.md5()
        hash.update(self.sending_date.isoformat())
        self.hash_code = hash.hexdigest()
        super(Newsletter, self).save()
        if self.is_published == False:
            default_articles = DefaultNewsletterContent.objects.all().order_by('order')
            for default_article in default_articles:
                try:
                    article = Article.objects.get(category=default_article.category, publication_date=self.sending_date) 
                except:
                    article = 0
                if article:
                    try:
                        c =  NewsletterContent.objects.get(newsletter=self, article=article)
                    except ObjectDoesNotExists:
                        c = NewsletterContent.objects.create(newsletter=self, order=default_article.order, article=article)
                        
    # Managers
    objects = models.Manager()



class NewsletterContent(models.Model):
    newsletter    = models.ForeignKey(Newsletter, verbose_name=_('newsletter'))
    order         = models.PositiveIntegerField(_('order'))
    article       = models.ForeignKey(Article, verbose_name=_('article'))
    clicked_count = models.PositiveIntegerField(_('clicked count'), default=0, editable=False)
        
    def __unicode__(self):
        return u'%s-%s-%s' % (self.newsletter, self.order, self.article)



class DefaultNewsletterContent(models.Model):
    order    = models.PositiveIntegerField(_('order'))
    category = models.ForeignKey(Category, verbose_name=_('category'))

    def __unicode__(self):
        return u'%s-%s' % (self.order, self.category)



class Subscriber(models.Model):
    email              = models.EmailField(_('email'), unique=True)
    hash_code          = models.CharField(_('hash code'), max_length=32, db_index=True, default="x", editable=False)
    subscribing_date   = models.DateTimeField(_('subscribing date'), null=True, blank=True)
    unsubscribing_date = models.DateTimeField(_('unsubscribing date'), null=True, blank=True)
    is_active          = models.BooleanField(_('active'), default=True)
    last_newsletter    = models.ForeignKey(Newsletter, verbose_name=_('last newsletter'), null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.email
        
    def save(self):
        hash = hashlib.md5()
        hash.update(self.email)
        self.hash_code = hash.hexdigest()
        super(Subscriber, self).save()


