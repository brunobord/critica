# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.notes`` application.

"""
from django.utils.translation import ugettext_lazy as _


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
POSITION_POSTIT = 1
POSITION_PUNAISE_LIGNE1_GAUCHE = 2
POSITION_PUNAISE_LIGNE1_DROITE = 3
POSITION_PUNAISE_LIGNE2_GAUCHE = 4
POSITION_PUNAISE_LIGNE2_DROITE = 5
POSITION_ACCORDEON_LIGNE1 = 6
POSITION_ACCORDEON_LIGNE2 = 7
POSITION_ACCORDEON_LIGNE3 = 8
POSITION_ACCORDEON_LIGNE4 = 9
POSITION_ACCORDEON_LIGNE5 = 10

NOTE_TYPE_POSITION_CHOICES = (
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

