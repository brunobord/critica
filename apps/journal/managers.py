"""
Managers for ``critica.apps.journal`` models.

"""
from django.db import models


class PublishedArticleManager(models.Manager):   
    def get_query_set(self):
        return super(PublishedArticleManager, self).get_query_set().filter(issues__is_complete=True, is_published=True, is_reserved=False)


class CompleteIssueManager(models.Manager):
    def get_query_set(self):
        return super(CompleteIssueManager, self).get_query_set().filter(is_complete=True)
        
    def published(self):
        return self.get_query_set().filter(is_published=True)


class PublishedIssueManager(models.Manager):
    def get_query_set(self):
        return super(PublishedIssueManager, self).get_query_set().filter(is_published=True)
        
    def complete(self):
        return self.get_query_set().filter(is_complete=True)


