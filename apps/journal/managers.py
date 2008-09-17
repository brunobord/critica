"""
Managers for ``critica.apps.journal`` models.

"""
from django.db import models
from critica.apps.journal import choices


class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set()

class IllustrationManager(models.Manager):
    def get_query_set(self):
        return super(IllustrationManager, self).get_query_set()

class ReportageManager(models.Manager):
    def get_query_set(self):
        return super(ReportageManager, self).get_query_set()

class ArticleManager(models.Manager):   
    def get_query_set(self):
        return super(ArticleManager, self).get_query_set().filter(issues__is_complete=True, status=choices.STATUS_PUBLISHED, is_reserved=False)

class IssueManager(models.Manager):
    def get_query_set(self):
        return super(IssueManager, self).get_query_set().filter(is_complete=True)


