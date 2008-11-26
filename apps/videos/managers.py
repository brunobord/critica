"""
Managers of ``critica.apps.videos`` models.

"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class VideoManager(models.Manager):
    """
    Base Manager
    
    """
    def get_query_set(self):
        """
        Default QuerySet.
        
        """
        return super(VideoManager, self).get_query_set()
            
    def issue_video(self, issue_id):
        """
        Returns video of a given issue.
        
        """
        qs = self.get_query_set().filter(issues__id=issue_id)
        try:
            qs = qs[0:1].get()
        except ObjectDoesNotExist:
            qs = None
        return qs


class VideoPublishedManager(VideoManager):
    """
    Published Videos Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(VideoPublishedManager, self).get_query_set().filter(
            is_ready_to_publish=True,
            is_reserved=False)


class VideoPreviewManager(VideoManager):
    """
    Preview Videos Manager.
    
    """
    def get_query_set(self):
        """
        QuerySet.
        
        """
        return super(VideoPreviewManager, self).get_query_set().filter(is_reserved=False)



