# -*- coding: utf-8 -*-
import os
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from critica.apps.categories.models import Category
from critica.apps.articles.models import Article
from critica.apps.anger.models import AngerArticle
from critica.apps.epicurien.models import EpicurienArticleType
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.positions.models import DefaultCategoryPosition
from critica.apps.positions.models import IssueCategoryPosition
from critica.apps.positions.models import DefaultNotePosition
from critica.apps.positions.models import IssueNotePosition
from critica.apps.quotas.models import DefaultCategoryQuota
from critica.apps.quotas.models import CategoryQuota
from critica.apps.notes.models import NoteType
from critica.apps.notes.models import Note
from critica.apps.regions.models import RegionNote
from critica.apps.regions.models import Region
from critica.apps.voyages.models import VoyagesArticle  
from critica.apps.issues.models import Issue
from critica.apps.utils import urlbase64

CATEGORY_MAP = [
    (1, 4010),
    (2, 4011),
    (3, 4002),
    (4, 4003),
    (5, 4004),
    (6, 4005),
    (7, 4006),
    (8, 4007),
    (9, 4008),
]

NOTE_TYPE_MAP = [
    (1, 4008),
    (2, 4004),
    (3, 4009),
    (4, 4003),
    (5, 4007),
    (6, 4001),
    (7, 4006),
    (8, 4010),
    (9, 4005),
    (10, 4002),
]

REGION_MAP = [
    (1, 4018),
    (2, 4004),
    (3, 4001),
    (4, 4005),
    (5, 4002),
    (6, 4006),
    (7, 4003),
    (8, 4007),
    (9, 4026),
    (10, 4011),
    (11, 4009),
    (12, 4012),
    (13, 4010),
    (14, 4013),
    (15, 4014),
    (16, 4015),
    (17, 4016),
    (18, 4017),
    (19, 4008),
    (20, 4025),
    (21, 4019),
    (22, 4020),
    (23, 4021),
    (24, 4022),
    (25, 4023),
    (26, 4024),
]

AUTHORS_TO_REMOVE = [
    4001, 
    4020,
]

REGIONS_TO_REMOVE = [
    4001,
    4002,
    4003,
    4004,
    4005,
    4006,
    4007,
    4008,
    4009,
    4010,
    4011,
    4012,
    4013,
    4014,
    4015,
    4016,
    4017,
    4018,
    4019,
    4020,
    4021,
    4022,
    4023,
    4024,
    4025,
    4026,
]

NOTE_TYPES_TO_REMOVE = [
    4001,
    4002,
    4003,
    4004,
    4005,
    4006,
    4007,
    4008,
    4009,
    4010,
]

CATEGORIES_TO_REMOVE = [
    4001,
    4002,
    4003,
    4004,
    4005,
    4006,
    4007,
    4008,
    4009,
    4010,
    4011,
    4012,
    4013,
    4014,
    4015,
]

class Command(NoArgsCommand):
    """
    Command that cleans archives.
    
    """
    def handle_noargs(self, **options):
        """
        Handler.
        
        """
        print "Loading fixtures..."
        self._initialize()

        print "\nANGER / ARTICLES COUP DE GUEULE"
        self._draw_separator()
        self.clean_anger()
        
        print "\nARTICLES / ARTICLES RUBRIQUES STANDARDS"
        self._draw_separator()
        self.clean_articles()
        
        print "\nEPICURIEN / ARTICLES EPICURIEN"
        self._draw_separator()
        self.clean_epicurien()

        print "\nILLUSTRATIONS"
        self._draw_separator()
        self.clean_illustrations()
        
        print "\nISSUES"
        self._draw_separator()
        self.clean_issues()

        print "\nNOTES / BREVES"
        self._draw_separator()
        self.clean_notes()

        print "\nREGION NOTES / BREVES REGIONNALES"
        self._draw_separator()
        self.clean_region_notes()
        
        print "\nVOYAGES / ARTICLES VOYAGES"
        self._draw_separator()
        self.clean_voyages()

        print "\nDELETE OBJECTS TO DELETE"
        self._draw_separator()
        self.delete_objects()
        
        print "\n"

    
    def clean_anger(self):
        print "Nothing yet..."
        
        
    def clean_articles(self):
        """
        Clean articles.
        
        """
        # Update categories
        # ----------------------------------------------------------------------
        for category in CATEGORY_MAP:
            articles = Article.objects.filter(category__id=category[1])
            for article in articles:
                new_category = Category.objects.get(id=category[0])
                article.category = new_category
                article.save()       
        print "Update categories... OK."
        
        # Set featured boolean
        # ----------------------------------------------------------------------
        self._set_featured(Article)


    def clean_epicurien(self):
        """
        Clean articles of "Epicurien" category.
        
        """        
        # Delete empty articles
        # ----------------------------------------------------------------------
        try:
            articles = EpicurienArticle.objects.filter(title__contains='titre indisponible')
            for article in articles:
                article.delete()
        except:
            pass
        print "Delete empty articles... OK."
        
        # Update types
        #
        # category id 4015: cote bar
        # category id 4013: cote gourmets
        # category id 4012: cote fumeurs
        #
        # Category is automatically updated at saving
        # ----------------------------------------------------------------------
        type_cotegourmets = EpicurienArticleType.objects.get(id=1)
        type_cotebar = EpicurienArticleType.objects.get(id=2)
        type_cotefumeurs = EpicurienArticleType.objects.get(id=3)

        articles_bar = EpicurienArticle.objects.filter(category__id=4015)
        for article in articles_bar:
            article.type = type_cotebar
            article.save()
        print "Update 'Cote bar' type... OK."
        
        articles_gourmets = EpicurienArticle.objects.filter(category__id=4013)
        for article in articles_gourmets:
            article.type = type_cotegourmets
            article.save()
        print "Update 'Cote Gourmets' type... OK."
            
        articles_fumeurs = EpicurienArticle.objects.filter(category__id=4012)
        for article in articles_fumeurs:
            article.type = type_cotefumeurs
            article.save()
        print "Update 'Cote fumeurs' type... OK."
        
        # Regroup issues
        # ----------------------------------------------------------------------
        self._regroup_issues(EpicurienArticle)


    def clean_illustrations(self):
        """
        Clean illustrations.
        
        """
        print "Nothing yet..."
        
        
    def clean_issues(self):
        """
        Clean issues.
        
        """        
        # Generate encoded secret keys
        # ----------------------------------------------------------------------
        issues = Issue.objects.all()
        for issue in issues:
            issue.secret_key = urlbase64.uri_b64encode(str(issue.number))
            issue.save()
        print "Generate secret keys... OK."
        
        # Generate positions
        # ----------------------------------------------------------------------        
        issues = Issue.objects.all()
        
        for issue in issues:
            # categories
            default_positions = DefaultCategoryPosition.objects.all()
            for default_position in default_positions:
                issue_position = IssueCategoryPosition(issue=issue, category=default_position.category, position=default_position.position)
                issue_position.save()
            # notes
            default_positions = DefaultNotePosition.objects.all()
            for default_position in default_positions:
                issue_position = IssueNotePosition(issue=issue, category=default_position.category, type=default_position.type, position=default_position.position)
                issue_position.save()
            # quotas
            default_quotas = DefaultCategoryQuota.objects.all()
            for default_quota in default_quotas:
                category = Category.objects.get(slug=default_quota.category.slug)
                category_quota = CategoryQuota(issue=issue, category=category, quota=default_quota.quota)
                category_quota.save()        
        print "Generate positions and quotas for all issues... OK."


    def clean_notes(self):
        """
        Clean notes.
        
        """        
        # Update categories
        # ----------------------------------------------------------------------
        for category in CATEGORY_MAP:
            notes = Note.objects.filter(category__id=category[1])
            for note in notes:
                new_category = Category.objects.get(id=category[0])
                note.category = new_category
                note.save()       
        print "Update categories... OK."

        # Update types
        # ----------------------------------------------------------------------
        for note_type in NOTE_TYPE_MAP:
            notes = Note.objects.filter(type__id=note_type[1])
            for note in notes:
                new_type = NoteType.objects.get(id=note_type[0])
                note.type = new_type
                note.save()
        print "Update types... OK."
        
        # Set featured boolean
        # ----------------------------------------------------------------------
        self._set_featured(Note)
        

    def clean_region_notes(self):
        """
        Clean region notes.
        
        """
        # Update regions
        # Category is automatically updated at saving
        # ----------------------------------------------------------------------
        for region in REGION_MAP:
            notes = RegionNote.objects.filter(region__id=region[1])
            for note in notes:
                new_region = Region.objects.get(id=region[0])
                note.region = new_region
                note.is_ready_to_publish = True
                note.is_reserved = False
                note.save()
        print "Update regions... OK."
        

    def clean_voyages(self):
        """
        Clean articles of "Voyages" category.
        
        """  
        self._regroup_issues(VoyagesArticle)


    def delete_objects(self):
        """
        Delete objects.
        
        """
        # AUTHORS
        # ----------------------------------------------------------------------
        for author in AUTHORS_TO_REMOVE:
            # articles to delete
            trash = []
            # articles
            articles = Article.objects.filter(author__id=author)
            trash.append(articles)
            # epicurien
            articles = EpicurienArticle.objects.filter(author__id=author)
            trash.append(articles)
            # voyages
            articles = VoyagesArticle.objects.filter(author__id=author)
            trash.append(articles)
            # anger
            articles = AngerArticle.objects.filter(author__id=author)
            trash.append(articles)
            # notes
            notes = Note.objects.filter(author__id=author)
            trash.append(notes)
            # region notes
            notes = RegionNote.objects.filter(author__id=author)
            trash.append(notes)
            # clean
            for item in trash:
                item.delete()
        print "Delete obsolete authors... OK."
        
        # REGIONS
        # ----------------------------------------------------------------------
        for region in REGIONS_TO_REMOVE:
            region = Region.objects.get(id=region)
            region.delete()
        print "Delete obsolete regions... OK."
        
        # NOTE TYPES
        # ----------------------------------------------------------------------
        for note_type in NOTE_TYPES_TO_REMOVE:
            note_type = NoteType.objects.get(id=note_type)
            note_type.delete()
        print "Delete obsolete note types... OK."
        
        # CATEGORIES
        # ----------------------------------------------------------------------
        for category in CATEGORIES_TO_REMOVE:
            category = Category.objects.get(id=category)
            category.delete()
        print "Delete obsolete categories... OK."


    def _draw_separator(self):
        """
        Draw article type separator.
        
        """
        print 80 * '-' + '\n'

    
    def _initialize(self):
        """
        Initialization.
        
        """
        load_fixtures = os.system('./manage.py loaddata data/archives/*')
        
    
    def _get_slugs(self, model):
        """
        Returns a list of model slugs.
        
        """
        slugs = []
        items = model.objects.all()
        for item in items:
            slugs.append(str(item.slug))
        slugs = list(set(slugs))
        return slugs

  
    def _regroup_issues(self, model):
        """
        Regroup issues of a model.
        
        """
        slugs = self._get_slugs(model)
        for slug in slugs:
            changed = False
            if changed == False:
                items = model.objects.filter(slug=slug)
                issues = []
                for item in items:
                    for issue in item.issues.all():
                        issues.append(issue)
                issues = list(set(issues))
                for issue in issues:
                    item.issues.add(issue)    
                    item.save()
                changed = True
        print "Regroup issues... OK."
        items = model.objects.all()
        for item in items:
            if len(item.issues.all()) < 2:
                item.delete()
        print "Delete extra articles... OK."
       
        
    def _set_featured(self, model):
        """
        Sets 'is_featured' field to True if item's title contains the word 'exclusif'.
        
        """
        items = model.objects.filter(title__icontains='exclusif')
        for item in items:
            item.is_featured = True
            item.save()
        print "Set featured... OK."


