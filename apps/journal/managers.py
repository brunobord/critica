"""
Managers for ``critica.apps.journal`` models.

"""
from django.db import models
from critica.apps.journal import choices


class PublishedArticleManager(models.Manager):
    def get_query_set(self):
        return super(PublishedArticleManager, self).get_query_set().filter(issues__status=choices.ISSUE_STATUS_COMPLETE, status=choices.ARTICLE_STATUS_PUBLISHED)


class CompleteIssueManager(models.Manager):
    def get_query_set(self):
        return super(CompleteIssueManager, self).get_query_set().filter(status=choices.ISSUE_STATUS_COMPLETE)


