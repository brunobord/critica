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
from django.contrib.auth.models import User
from critica.apps.users.models import UserNickname

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

USER_MAP = [
    # Charlotte David / Rédaction Critica / Bidule Plop
    (11, 14, 4000),
    # Charlotte David / Rédaction Critica / Rédaction de Critica
    (11, 14, 4004),
    # Gracianne Hastoy / NULL / Gracianne Hastoy
    (10, None, 4002),
    # Emanuelle Morin / NULL / Emanuelle Morin
    (8, None, 4003),
    # Jean Chalvidant / Pierre Arandel / Pierre Arandel
    (6, 18, 4005),
    # Bruno Cavalié / NULL / Bruno Cavalié
    (7, None, 4006),
    # Sébastien Soumagnas / Ned Euphorya / Ned Euphorya
    (12, 16, 4007),
    # Charlotte David / NULL / Charlotte David
    (11, None, 4008),
    # Bruno Cavalié / King Charle / King Charle
    (7, 5, 4009),
    # Emanuelle Morin / Nathalie d'Armagnac / Nathalie d'Armagnac
    (8, 4, 4010),
    # Jean Chalvidant / NULL / Jean Chalvidant
    (6, None, 4011),
    # Karen Jouault / NULL / Karen Jouault
    (9, None, 4012),
    # Charlotte David / Sarah Cianengoty / Sarah Cianengoty
    (11, 9, 4013),
    # Gracianne Hastoy / Yoanna Grishac / Yoanna Grishac
    (10, 20, 4014),
    # Karen Jouault / Emily Bignon / Emily Bignon
    (9, 1, 4015),
    # Dominique Larue / NULL / Dominique Larue
    (19, None, 4016),
    # Bruno Cavalié / Paul Fernando / Paul Fernando
    (7, 17, 4017),
    # Aurore Labarbe / NULL / Aurore Labarbe
    (5, None, 4018),
    # Karen Jouault / Dominique Podovani / Dominique Podovani   
    (9, 3, 4019),
    # Charlotte David / Rédaction Critica / Maïlys
    (11, 14, 4020),
    # Charlotte David / Rédaction Critica / Eric Laborde
    (11, 14, 4022),
    # Sébastien Soumagnas / NULL / Sébastien Soumagnas
    (12, None, 4023),
]

USERS_AND_ARTICLES_BY_TO_REMOVE = [
    4001, 
    4020,
]

USERS_TO_REMOVE = [
    4000,
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
        self.load_fixtures()

        print "\nANGER / ARTICLES COUP DE GUEULE"
        self._draw_separator()
        self.update_anger()
        
        print "\nARTICLES / ARTICLES RUBRIQUES STANDARDS"
        self._draw_separator()
        self.update_articles()
        
        print "\nEPICURIEN / ARTICLES EPICURIEN"
        self._draw_separator()
        self.update_epicurien()

        print "\nILLUSTRATIONS"
        self._draw_separator()
        self.update_illustrations()
        
        print "\nISSUES"
        self._draw_separator()
        self.update_issues()

        print "\nNOTES / BREVES"
        self._draw_separator()
        self.update_notes()

        print "\nREGION NOTES / BREVES REGIONNALES"
        self._draw_separator()
        self.update_region_notes()
        
        print "\nVOYAGES / ARTICLES VOYAGES"
        self._draw_separator()
        self.update_voyages()

        print "\nAUTHORS AND NICKNAMES"
        self._draw_separator()
        self.update_authors_and_nicknames()

        print "\nDELETE OBJECTS TO DELETE"
        self._draw_separator()
        self.delete_objects()

        print "\nGENERATE NEW DUMPS"
        self._draw_separator()
        self.generate_new_dumps()

        print "\n"

    
    def update_authors_and_nicknames(self):
        """
        Update authors (users) and nicknames.
        
        """
        for user in USER_MAP:
            # author / author_nickname
            author = User.objects.get(id=user[0])
            author_nickname = None
            if user[1]:
                author_nickname = UserNickname.objects.get(id=user[1])
            # articles
            articles = Article.objects.filter(author__id=user[2])
            for article in articles:
                article.author = author
                article.author_nickname = author_nickname
                article.save()
            # epicurien
            articles = EpicurienArticle.objects.filter(author__id=user[2])
            for article in articles:
                article.author = author
                article.author_nickname = author_nickname
                article.save()
            # voyages
            articles = VoyagesArticle.objects.filter(author__id=user[2])
            for article in articles:
                article.author = author
                article.author_nickname = author_nickname
                article.save()
            # anger
            articles = AngerArticle.objects.filter(author__id=user[2])
            for article in articles:
                article.author = author
                article.author_nickname = author_nickname
                article.save()
            # notes
            notes = Note.objects.filter(author__id=user[2])
            for note in notes:
                note.author = author
                note.author_nickname = author_nickname
                note.save()
            # region notes
            notes = RegionNote.objects.filter(author__id=user[2])
            for note in notes:
                note.author = author
                note.author_nickname = author_nickname
                note.save()
        print "Update authors and nicknames... OK."
        
        
    def update_anger(self):
        """
        Update anger articles.
        
        """
        # Update categories
        # ----------------------------------------------------------------------
        articles = AngerArticle.objects.all()
        category = Category.objects.get(id=13)
        for article in articles:
            article.category = category
            article.save()
        print "Update categories... OK."
        
        
    def update_articles(self):
        """
        Update articles.
        
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


    def update_epicurien(self):
        """
        Update articles of "Epicurien" category.
        
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


    def update_illustrations(self):
        """
        Update illustrations.
        
        """
        print "Nothing yet..."
        
        
    def update_issues(self):
        """
        Update issues.
        
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


    def update_notes(self):
        """
        Update notes.
        
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
        

    def update_region_notes(self):
        """
        Update region notes.
        
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
        

    def update_voyages(self):
        """
        Update articles of "Voyages" category.
        
        """  
        self._regroup_issues(VoyagesArticle)


    def delete_objects(self):
        """
        Delete objects.
        
        """
        # AUTHORS
        # ----------------------------------------------------------------------
        for author in USERS_AND_ARTICLES_BY_TO_REMOVE:
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
        
        # USERS
        # ----------------------------------------------------------------------
        for user in USERS_TO_REMOVE:
            user = User.objects.get(id=user)
            user.delete()
        print "Delete obsolete users... OK."


    def load_fixtures(self):
        """
        Load fixtures.
        
        """
        os.system('./manage.py loaddata user_data')
        os.system('./manage.py loaddata data/archives/*')
        

    def generate_new_dumps(self):
        """
        Generate new JSON dump files.
        
        """
        os.system('rm -f data/clean_archives/*')
        print "Delete old dumps... OK."
        os.system('./manage.py dumpdata anger --indent=4 > data/clean_archives/anger.json')
        print "Generate dump: anger... OK."
        os.system('./manage.py dumpdata articles --indent=4 > data/clean_archives/articles.json')
        print "Generate dump: articles... OK."
        os.system('./manage.py dumpdata epicurien --indent=4 > data/clean_archives/epicurien.json')
        print "Generate dump: epicurien... OK."
        os.system('./manage.py dumpdata illustrations --indent=4 > data/clean_archives/illustrations.json')
        print "Generate dump: illustrations... OK."
        os.system('./manage.py dumpdata issues --indent=4 > data/clean_archives/issues.json')
        print "Generate dump: issues... OK."
        os.system('./manage.py dumpdata notes --indent=4 > data/clean_archives/notes.json')
        print "Generate dump: notes... OK."
        os.system('./manage.py dumpdata regions --indent=4 > data/clean_archives/regions_notes.json')
        print "Generate dump: regions notes... OK."
        os.system('./manage.py dumpdata voyages --indent=4 > data/clean_archives/voyages.json')
        print "Generate dump: voyages... OK."


    def _draw_separator(self):
        """
        Draw article type separator.
        
        """
        print 80 * '-' + '\n'

    
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


