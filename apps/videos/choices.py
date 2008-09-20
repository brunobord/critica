# -*- coding: utf-8 -*-
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

