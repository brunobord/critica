# -*- coding: utf-8 -*-
"""
Choices of ``critica.apps.journal`` application.

"""
from django.utils.translation import ugettext_lazy as _


# Status
# ------------------------------------------------------------------------------
STATUS_PUBLISHED = 1
STATUS_DRAFT = 2

STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Ready to publish')),
    (STATUS_DRAFT, _('Draft')),
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


