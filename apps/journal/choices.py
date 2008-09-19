# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.journal`` application.

"""
from django.utils.translation import ugettext_lazy as _


# Issue status
# ------------------------------------------------------------------------------
ISSUE_STATUS_PUBLISHED = 1
ISSUE_STATUS_COMPLETE = 2
ISSUE_STATUS_NEW = 3

ISSUE_STATUS_CHOICES = (
    (ISSUE_STATUS_PUBLISHED, _('Published')),
    (ISSUE_STATUS_COMPLETE, _('Complete')),
    (ISSUE_STATUS_NEW, _('New')),
)

# Reportage status
# ------------------------------------------------------------------------------
REPORTAGE_STATUS_PUBLISHED = 1
REPORTAGE_STATUS_PENDING_PUBLICATION = 2
REPORTAGE_STATUS_NEW = 3
REPORTAGE_STATUS_RESERVED = 4

REPORTAGE_STATUS_CHOICES = (
    (REPORTAGE_STATUS_PUBLISHED, _('Published')),
    (REPORTAGE_STATUS_PENDING_PUBLICATION, _('Ready to be published')),
    (REPORTAGE_STATUS_NEW, _('New')),
    (REPORTAGE_STATUS_RESERVED, _('Reserved')),
)

# Article status
# ------------------------------------------------------------------------------
ARTICLE_STATUS_PUBLISHED = 1 
ARTICLE_STATUS_PENDING_PUBLICATION = 2
ARTICLE_STATUS_NEW = 3
ARTICLE_STATUS_RESERVED = 4

ARTICLE_STATUS_CHOICES = (
    (ARTICLE_STATUS_PUBLISHED, _('Published')),
    (ARTICLE_STATUS_PENDING_PUBLICATION, _('Ready to be published')),
    (ARTICLE_STATUS_NEW, _('New')),
    (ARTICLE_STATUS_RESERVED, _('Reserved')),
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

# Positions
# ------------------------------------------------------------------------------
CATEGORY_POSITION_CHOICES = (
    (1, 'Cadre haut'),
    (2, 'Cadre bas'),
    (3, 'Post-it'),
    (4, 'Punaise -- ligne 1 -- gauche'),
    (5, 'Punaise -- ligne 1 -- droite'),
    (6, 'Punaise -- ligne 2 -- gauche'),
    (7, 'Punaise -- ligne 2 -- droite'),
    (8, 'Punaise -- ligne 3 -- gauche'),
    (9, 'Punaise -- ligne 3 -- droite'),
    (10, 'Punaise -- ligne 4 -- gauche'),
    (12, 'Punaise -- ligne 4 -- droite'),
    (13, 'Scotch'),
)

NOTE_TYPE_GENERAL_POSITION_CHOICES = (
    (1, 'Post-it'),
    (2, 'Punaise -- ligne 1 -- gauche'),
    (3, 'Punaise -- ligne 1 -- droite'),
    (4, 'Punaise -- ligne 2 -- gauche'),
    (5, 'Punaise -- ligne 2 -- droite'),
    (6, 'Accordéon -- ligne 1'),
    (7, 'Accordéon -- ligne 2'),
    (8, 'Accordéon -- ligne 3'),
    (9, 'Accordéon -- ligne 4'),
    (10, 'Accordéon -- ligne 5'),
)

