# -*- coding: utf-8 -*-
""" 
Administration interface options for ``critica.apps.issues`` models. 

"""
from django.contrib import admin
from critica.apps.admin.sites import basic_site, advanced_site
from critica.apps.issues.models import Issue
from critica.apps.positions.models import CategoryPosition


class CategoryPositionInline(admin.TabularInline):
    """
    Category position inline for ``Issue`` model.
    
    """
    model = CategoryPosition
    max_num = 13
    
    
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
    inlines = [CategoryPositionInline]

    def save_model(self, request, obj, form, change):
        obj.save()
        from django.conf import settings
        from critica.apps.categories.models import Category
        from critica.apps.positions.models import CategoryPosition
        from critica.apps.positions import settings as positions_settings
        # Auto-creates categories
        if 'critica.apps.categories' in settings.INSTALLED_APPS:
            # national
            category = Category.objects.get(slug='national')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_NATIONAL)
            position.save()
            # etranger
            category = Category.objects.get(slug='etranger')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_ETRANGER)
            position.save()
            # bouquins
            category = Category.objects.get(slug='bouquins')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_BOUQUINS)
            position.save()
            # societe
            category = Category.objects.get(slug='societe')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_SOCIETE)
            position.save()
            # nanas
            category = Category.objects.get(slug='nanas')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_NANAS)
            position.save()
            # sports
            category = Category.objects.get(slug='sports')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_SPORTS)
            position.save()
            # télé
            category = Category.objects.get(slug='tele')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_TELE)
            position.save()
            # pipoles
            category = Category.objects.get(slug='pipoles')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_PIPOLE)
            position.save()
            # insolite
            category = Category.objects.get(slug='insolite')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_INSOLITE)
            position.save()
            # regions
            category = Category.objects.get(slug='regions')
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_REGIONS)
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
            position = CategoryPosition(issue=obj, category=category, position=positions_settings.CATEGORY_DEFAULT_POSITION_COUP_DE_GUEULE)
            position.save()

admin.site.register(Issue, IssueAdmin)
basic_site.register(Issue, IssueAdmin)
advanced_site.register(Issue, IssueAdmin)


