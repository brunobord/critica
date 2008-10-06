"""
Managers for ``critica.apps.issues`` models.

"""
from django.db import models


class PublishedIssueManager(models.Manager):
    def get_query_set(self):
        return super(PublishedIssueManager, self).get_query_set().filter(is_published=True)


