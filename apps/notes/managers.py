"""
Managers of ``critica.apps.notes`` application.

"""
from django.db import models


class NotePublishedManager(models.Manager):
    def get_query_set(self):
        return super(NotePublishedManager, self).get_query_set().filter(
            issues__is_published=True, 
            is_ready_to_publish=True,
            is_reserved=False)


class NotePreviewManager(models.Manager):
    def get_query_set(self):
        return super(NotePreviewManager, self).get_query_set().filter(is_reserved=False)
