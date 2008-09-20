"""
Managers for ``critica.apps.video`` models.

"""
from django.db import models
from critica.apps.videos.models import Video


class PublishedVideoManager(models.Manager):
    def get_query_set(self):
        return super(PublishedVideoManager, self).get_query_set().filter(status=Video.STATUS_PUBLISHED)


