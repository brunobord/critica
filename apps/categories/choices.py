# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.categories`` application.

"""
from django.utils.translation import ugettext_lazy as _


# Positions
# ------------------------------------------------------------------------------
POSITION_CADRE_HAUT = 1
POSITION_CADRE_BAS = 2
POSITION_POSTIT = 3
POSITION_PUNAISE_LIGNE1_GAUCHE = 4
POSITION_PUNAISE_LIGNE1_DROITE = 5
POSITION_PUNAISE_LIGNE2_GAUCHE = 6
POSITION_PUNAISE_LIGNE2_DROITE = 7
POSITION_PUNAISE_LIGNE3_GAUCHE = 8
POSITION_PUNAISE_LIGNE3_DROITE = 9
POSITION_PUNAISE_LIGNE4_GAUCHE = 10
POSITION_PUNAISE_LIGNE4_DROITE = 11
POSITION_SCOTCH = 12

POSITION_CHOICES = (
    (POSITION_CADRE_HAUT, 'Cadre haut'),
    (POSITION_CADRE_BAS, 'Cadre bas'),
    (POSITION_POSTIT, 'Post-it'),
    (POSITION_PUNAISE_LIGNE1_GAUCHE, 'Punaise -- ligne 1 -- gauche'),
    (POSITION_PUNAISE_LIGNE1_DROITE, 'Punaise -- ligne 1 -- droite'),
    (POSITION_PUNAISE_LIGNE2_GAUCHE, 'Punaise -- ligne 2 -- gauche'),
    (POSITION_PUNAISE_LIGNE2_DROITE, 'Punaise -- ligne 2 -- droite'),
    (POSITION_PUNAISE_LIGNE3_GAUCHE, 'Punaise -- ligne 3 -- gauche'),
    (POSITION_PUNAISE_LIGNE3_DROITE, 'Punaise -- ligne 3 -- droite'),
    (POSITION_PUNAISE_LIGNE4_GAUCHE, 'Punaise -- ligne 4 -- gauche'),
    (POSITION_PUNAISE_LIGNE4_DROITE, 'Punaise -- ligne 4 -- droite'),
    (POSITION_SCOTCH, 'Scotch'),
)

