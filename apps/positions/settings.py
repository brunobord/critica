# -*- coding: utf-8 -*-
"""
Settings of ``critica.apps.positions``.

"""
from apps.positions import choices


# Default category order
# ------------------------------------------------------------------------------
CATEGORY_DEFAULT_ORDER = [
    'national',
    'etranger',
    'bouquins',
    'societe',
    'nanas',
    'sports',
    'tele',
    'pipoles',
    'insolite',
    'regions',
    'epicurien',
    'voyages',
    'coup-de-gueule'
]

# Default category positions
# ------------------------------------------------------------------------------
CATEGORY_DEFAULT_POSITION = {
    'national': choices.CATEGORY_POSITION_CADRE_HAUT,
    'etranger': choices.CATEGORY_POSITION_CADRE_BAS,
    'bouquins': choices.CATEGORY_POSITION_POSTIT,
    'societe': choices.CATEGORY_POSITION_PUNAISE_LIGNE1_GAUCHE,
    'nanas': choices.CATEGORY_POSITION_PUNAISE_LIGNE1_DROITE,
    'sports': choices.CATEGORY_POSITION_PUNAISE_LIGNE2_GAUCHE,
    'tele': choices.CATEGORY_POSITION_PUNAISE_LIGNE2_DROITE,
    'pipoles': choices.CATEGORY_POSITION_PUNAISE_LIGNE3_GAUCHE,
    'insolite': choices.CATEGORY_POSITION_PUNAISE_LIGNE3_DROITE,
    'regions': choices.CATEGORY_POSITION_PUNAISE_LIGNE4_GAUCHE,
    'coup-de-gueule': choices.CATEGORY_POSITION_SCOTCH,
}

# Excluded categories
# ------------------------------------------------------------------------------
EXCLUDED_CATEGORIES = [
    'regions',
    'epicurien',
    'voyages',
    'coup-de-gueule',
]

# Default note type order
# ------------------------------------------------------------------------------
NOTE_TYPE_DEFAULT_ORDER = [
    'vous-saviez',
    'premiere-nouvelle',
    'on-sen-serait-passe',
    'on-en-rirait-presque',
    'ils-ont-ose',
    'linfo-off',
    'fallait-sen-douter',
    'criticons',
    'ca-cest-fait',
    'aucun-interet',
]

# Default note type positions
# ------------------------------------------------------------------------------
NOTE_TYPE_DEFAULT_POSITION = {
    'vous-saviez': choices.NOTE_TYPE_POSITION_POSTIT,
    'premiere-nouvelle': choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE1_GAUCHE,
    'on-sen-serait-passe': choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE1_DROITE,
    'on-en-rirait-presque': choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE2_GAUCHE,
    'ils-ont-ose': choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE2_DROITE,
    'linfo-off': choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE1,
    'fallait-sen-douter': choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE2,
    'criticons': choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE3,
    'ca-cest-fait': choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE4,
    'aucun-interet': choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE5,
}

