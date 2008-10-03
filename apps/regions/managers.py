# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.notes_region`` application.

"""
from django.db import models
from critica.apps.issues import choices as issues_choices


class PublishedNoteManager(models.Manager):
    """
    Published notes.
    
    """
    def get_query_set(self):
        """
        By default, returns only ready to publish and not reserved notes
        from complete issues.
        
        """
        return super(PublishedNoteManager, self).get_query_set().filter(
            issues__is_published=True, 
            is_ready_to_publish=True,
            is_reserved=False,
        )


