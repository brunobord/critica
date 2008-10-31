# -*- coding: utf-8 -*-
"""
Models for ``critica.apps.polls`` application.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tagging.fields import TagField
from critica.apps.polls.managers import PollPublishedManager


class Poll(models.Model):
    """
    Poll.
    
    """
    submitter         = models.ForeignKey('auth.User', verbose_name=_('submitter'))
    title             = models.CharField(_('title'), max_length=255, unique=True, help_text=_('255 characters max.'))
    slug              = models.SlugField(_('slug'), blank=True, editable=False)
    creation_date     = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True, editable=False)
    issues            = models.ManyToManyField('issues.Issue', verbose_name=_('issues'), blank=True, db_index=True, help_text=_('Please, select one or several issues.'))
    tags              = TagField(verbose_name=_('tags'), help_text=_('Please, enter tags separated by commas or spaces.'))
    is_published      = models.BooleanField(_('published'), default=False, db_index=True, help_text=_('Is it ready to be published?'))

    objects   = models.Manager()
    published = PollPublishedManager()
    
    
    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('poll')
        verbose_name_plural = _('polls')


    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.title


    def save(self):
        """ 
        Object pre-saving / post-saving operations.
        
        """
        self.slug = slugify(self.title)
        super(Poll, self).save()



class Choice(models.Model):
    """
    Choice.
     
    """
    poll   = models.ForeignKey(Poll, verbose_name=_('poll'), help_text=_('Please, select or add a new poll.'))
    choice = models.CharField(_('choice'), max_length=200, help_text=_('Enter a choice for this poll.'))
    
    objects = models.Manager()


    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('choice')
        verbose_name_plural = _('choices')


    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.choice


    def get_vote_percentage(self):
        """
        Returns number of votes in percentage.
        
        """
        poll_count = self.poll.vote_set.all().count()
        choice_count = self.vote_set.all().count()
        percentage = (1.0 * choice_count / poll_count) * 100
        return round(percentage)



class Vote(models.Model):
    """
    Vote.
    
    """
    poll          = models.ForeignKey(Poll, verbose_name=_('poll'))
    choice        = models.ForeignKey(Choice, verbose_name=_('choice'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    ip_address    = models.IPAddressField(verbose_name=_('Submitter IP address'))


    class Meta:
        """ 
        Model metadata. 
        
        """
        verbose_name        = _('vote')
        verbose_name_plural = _('votes')
        get_latest_by       = 'creation_date'
        
        
    def __unicode__(self):
        """ 
        Object human-readable string representation. 
        
        """
        return u'%s' % self.choice.choice


