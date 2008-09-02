"""
Managers for ``critica.apps.journal`` models.

"""
from django.db import models


class CategoryManager(models.Manager):
    """
    ``Category`` model manager. 
    By default, retrieves all categories.
    
    """
    
    def get_query_set(self):
        """ Retrieves all categories. """
        return super(CategoryManager, self).get_query_set()



class PositionManager(models.Manager):
    """
    ``Position`` model manager.
    By default, retrieves all positions.
    
    """
    
    def get_query_set(self):
        """ Retrieves all positions. """
        return super(PositionManager, self).get_query_set()



class IllustrationManager(models.Manager):
    """
    ``Illustration`` model manager.
    By default, retrieves all illustrations.
    
    """
    
    def get_query_set(self):
        """ Retrieves all illustrations. """
        return super(IllustrationManager, self).get_query_set()



class ArticleManager(models.Manager):
    """
    ``Article`` model manager.
    By default, retrieves complete articles.
    
    """
    
    def get_query_set(self):
        """ Retrieves complete articles. """
        return super(ArticleManager, self).get_query_set().filter(is_published=True, is_illustrated=True)



class IssueManager(models.Manager):
    """
    ``Issue`` model manager.
    By default, retrieves complete issues.
    
    """
    
    def get_query_set(self):
        """ Retrieves complete issues. """
        return super(IssueManager, self).get_query_set().filter(is_complete=True)



class PageManager(models.Manager):
    """
    ``Page`` model manager.    
    By default, retrieves complete pages.
    
    """
    
    def get_query_set(self):
        """ Retrieves complete pages. """
        return super(PageManager, self).get_query_set().filter(is_complete=True)


