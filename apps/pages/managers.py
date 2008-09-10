"""
Managers for ``critica.apps.pages`` models.

"""
from django.db import models


class PageManager(models.Manager):
    """
    ``Page`` model manager.
    By default, retrieves published pages.
    
    """
    
    def get_query_set(self):
        """ Retrieves published pages. """
        return super(PageManager, self).get_query_set().filter(is_published=True)


