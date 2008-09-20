"""
Managers for ``critica.apps.notes_region`` models.

"""
from django.db import models
from critica.apps.articles import choices as articles_choices
from critica.apps.issues import choices as issues_choices


class PublishedNoteRegionManager(models.Manager):
    def get_query_set(self):
        return super(PublishedNoteRegionManager, self).get_query_set().filter(issues__status=issues_choices.STATUS_COMPLETE, status=articles_choices.STATUS_PUBLISHED)


