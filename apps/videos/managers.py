"""
Managers for ``critica.apps.video`` models.

"""
from django.db import models


class VideoPublishedManager(models.Manager):
    """
    Manager of published videos.
    
    """
    def get_query_set(self):
        """
        Default QuerySet.
        
        """
        return super(VideoPublishedManager, self).get_query_set().filter(
            is_ready_to_publish=True,
            is_reserved=False,
        )


