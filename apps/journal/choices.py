# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.journal`` application.

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

# Note types
# ------------------------------------------------------------------------------
NOTE_TYPE_CHOICES = (
    (1, "Vous saviez"),
    (2, "L'info off"),
    (3, "Fallait s'en douter"),
    (4, "Criti...cons"),
    (5, "Ça, c'est fait !"),
    (6, "Première nouvelle"),
    (7, "On s'en serait passé"),
    (8, "On en rirait presque"),
    (9, "Ils ont osé"),
    ("Régions",
        (
            (10, "Haute-Normandie"),
            (11, "Lorraine"),
            (12, "Île-de-France"),
            (13, "Midi-Pyrénées"),
            (14, "Languedoc-Roussillon"),
            (15, "Nord-Pas-de-Calais"),
            (16, "Limousin"),
            (17, "Pays de la Loire"),
            (18, "Alsace"),
            (19, "Basse-Normandie"),
            (20, "Aquitaine"),
            (21, "Bourgogne"),
            (22, "Auvergne"),
            (23, "Bretagne"),
            (24, "Centre"),
            (25, "Champagne-Ardenne"),
            (26, "Corse"),
            (27, "Franche-Comté"),
            (28, "Picardie"),
            (29, "Poitou-Charentes"),
            (30, "Provence-Alpes-Côte d'Azur"),
            (31, "Rhône-Alpes"),
            (32, "Guadeloupe"),
            (33, "Guyane"),
            (34, "Martinique"),
            (35, "Réunion"),
        )
    ),
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

NOTE_TYPE_REGION_POSITION_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
    (12, '12'),
    (13, '13'),
    (14, '14'),
    (15, '15'),
    (16, '16'),
    (17, '17'),
    (18, '18'),
    (19, '19'),
    (20, '20'),
    (21, '21'),
    (22, '22'),
    (23, '23'),
    (24, '24'),
    (25, '25'),
    (26, '26'),
)
