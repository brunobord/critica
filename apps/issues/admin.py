# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue
from critica.apps.categories.models import CategoryPosition
from critica.apps.notes.models import NoteTypePosition
from critica.apps.notes_region.models import NoteRegionFeatured


class CategoryPositionInline(admin.TabularInline):
    """
    Category position inline for ``Issue`` model.
    
    """
    model = CategoryPosition
    max_num = 13


class NoteTypePositionInline(admin.TabularInline):
    """
    Note type position inline for ``Issue`` model.
    
    """
    model = NoteTypePosition
    max_num = 10
    

class NoteRegionFeaturedInline(admin.TabularInline):
    """
    Featured region note inline for ``Issue`` model.
    
    """
    model = NoteRegionFeatured
    max_num = 1


class IssueAdmin(admin.ModelAdmin):
    """
    Administration interface for ``Issue`` model.
    
    """
    list_display = ('number', 'publication_date', 'status')
    list_filter = ('status',)
    search_fields = ('number',)
    ordering = ('-publication_date',)
    radio_fields = {'status': admin.VERTICAL}
    date_hierarchy = 'publication_date'
    
    # Inlines depend of installed applications
    from django.conf import settings
    inlines = []
    if 'critica.apps.categories' in settings.INSTALLED_APPS:
        inlines.append(CategoryPositionInline)
    if 'critica.apps.notes' in settings.INSTALLED_APPS:
        inlines.append(NoteTypePositionInline)
    if 'critica.apps.notes_region' in settings.INSTALLED_APPS:
        inlines.append(NoteRegionFeaturedInline)
        
    def save_model(self, request, obj, form, change):
        obj.save()
        from django.conf import settings
        # Auto-creates categories
        if 'critica.apps.categories' in settings.INSTALLED_APPS:
            from critica.apps.categories.models import Category, CategoryPosition
            from critica.apps.categories import settings as categories_settings
            # national
            category = Category.objects.get(slug='national')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_NATIONAL)
            position.save()
            # etranger
            category = Category.objects.get(slug='etranger')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_ETRANGER)
            position.save()
            # bouquins
            category = Category.objects.get(slug='bouquins')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_BOUQUINS)
            position.save()
            # societe
            category = Category.objects.get(slug='societe')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_SOCIETE)
            position.save()
            # nanas
            category = Category.objects.get(slug='nanas')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_NANAS)
            position.save()
            # sports
            category = Category.objects.get(slug='sports')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_SPORTS)
            position.save()
            # télé
            category = Category.objects.get(slug='tele')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_TELE)
            position.save()
            # pipoles
            category = Category.objects.get(slug='pipoles')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_PIPOLE)
            position.save()
            # insolite
            category = Category.objects.get(slug='insolite')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_INSOLITE)
            position.save()
            # regions
            category = Category.objects.get(slug='regions')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_REGIONS)
            position.save()
            # epicurien
            category = Category.objects.get(slug='epicurien')
            position = CategoryPosition(issue=obj, category=category)
            position.save()
            # voyage
            category = Category.objects.get(slug='voyages')
            position = CategoryPosition(issue=obj, category=category)
            position.save()
            # coup de gueule
            category = Category.objects.get(slug='coup-de-gueule')
            position = CategoryPosition(issue=obj, category=category, position=categories_settings.DEFAULT_POSITION_COUP_DE_GUEULE)
            position.save()
            
        # Auto-creates note types
        if 'critica.apps.notes' in settings.INSTALLED_APPS:
            from critica.apps.notes.models import NoteType, NoteTypePosition
            from critica.apps.notes import settings as notes_settings
            # vous saviez ?
            note_type = NoteType.objects.get(slug='premiere-nouvelle')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_VOUS_SAVIEZ)
            position.save()
            # première nouvelle
            note_type = NoteType.objects.get(slug='vous-saviez')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_PREMIERE_NOUVELLE)
            position.save()
            # on s'en serait passé
            note_type = NoteType.objects.get(slug='on-sen-serait-passe')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_ON_SEN_SERAIT_PASSE)
            position.save()
            # on en rirait presque
            note_type = NoteType.objects.get(slug='on-en-rirait-presque')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_ON_EN_RIRAIT_PRESQUE)
            position.save()
            # ils ont osé
            note_type = NoteType.objects.get(slug='ils-ont-ose')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_ILS_ONT_OSE)
            position.save()
            # l'info off
            note_type = NoteType.objects.get(slug='linfo-off')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_LINFO_OFF)
            position.save()
            # fallait s'en douter
            note_type = NoteType.objects.get(slug='fallait-sen-douter')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_FALLAIT_SEN_DOUTER)
            position.save()
            # criticons
            note_type = NoteType.objects.get(slug='criticons')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_CRITICONS)
            position.save()
            # ça, c'est fait
            note_type = NoteType.objects.get(slug='ca-cest-fait')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_CA_CEST_FAIT)
            position.save()
            # aucun intérêt
            note_type = NoteType.objects.get(slug='aucun-interet')
            position = NoteTypePosition(issue=obj, type=note_type, position=notes_settings.DEFAULT_POSITION_AUCUN_INTERET)
            position.save()

basic_site.register(Issue, IssueAdmin)
advanced_site.register(Issue, IssueAdmin)


