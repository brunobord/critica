# -*- coding: utf-8 -*-
"""
Settings of ``critica.apps.positions``.

"""
from critica.apps.positions import choices

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

# Default note type positions
# ------------------------------------------------------------------------------
NOTE_TYPE_DEFAULT_POSITION_VOUS_SAVIEZ = choices.NOTE_TYPE_POSITION_POSTIT
NOTE_TYPE_DEFAULT_POSITION_PREMIERE_NOUVELLE = choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE1_GAUCHE
NOTE_TYPE_DEFAULT_POSITION_ON_SEN_SERAIT_PASSE = choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE1_DROITE
NOTE_TYPE_DEFAULT_POSITION_ON_EN_RIRAIT_PRESQUE = choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE2_GAUCHE
NOTE_TYPE_DEFAULT_POSITION_ILS_ONT_OSE = choices.NOTE_TYPE_POSITION_PUNAISE_LIGNE2_DROITE
NOTE_TYPE_DEFAULT_POSITION_LINFO_OFF = choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE1
NOTE_TYPE_DEFAULT_POSITION_FALLAIT_SEN_DOUTER = choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE2
NOTE_TYPE_DEFAULT_POSITION_CRITICONS = choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE3
NOTE_TYPE_DEFAULT_POSITION_CA_CEST_FAIT = choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE4
NOTE_TYPE_DEFAULT_POSITION_AUCUN_INTERET = choices.NOTE_TYPE_POSITION_ACCORDEON_LIGNE5
