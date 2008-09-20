# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.issues`` application.

"""
from django.utils.translation import ugettext_lazy as _


# Status
# ------------------------------------------------------------------------------
STATUS_PUBLISHED = 1
STATUS_COMPLETE = 2
STATUS_NEW = 3

STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Published')),
    (STATUS_COMPLETE, _('Complete')),
    (STATUS_NEW, _('New')),
)

