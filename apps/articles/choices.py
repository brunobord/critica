# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.articles`` application.

"""
from django.utils.translation import ugettext_lazy as _


# Status
# ------------------------------------------------------------------------------
STATUS_PUBLISHED = 1 
STATUS_PENDING_PUBLICATION = 2
STATUS_NEW = 3
STATUS_RESERVED = 4

STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Published')),
    (STATUS_PENDING_PUBLICATION, _('Ready to be published')),
    (STATUS_NEW, _('New')),
    (STATUS_RESERVED, _('Reserved')),
)

# Opinions
# ------------------------------------------------------------------------------
OPINION_LIKE = 1
OPINION_DISLIKE = 2
OPINION_HAPPY = 3
OPINION_NOTHAPPY = 4

OPINION_CHOICES = (
    (OPINION_LIKE, _('I like')),
    (OPINION_DISLIKE, _('I dislike')),
    (OPINION_HAPPY, _("I'm happy")),
    (OPINION_NOTHAPPY, _("I'm not happy")),
)

