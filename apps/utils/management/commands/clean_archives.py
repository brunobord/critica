# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError


class Command(NoArgsCommand):
    """
    Command that cleans archives.
    
    """
    def handle_noargs(self, **options):
        """
        Handler.
        
        """
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

        print "\nNOTES / BREVES"
        self._draw_separator()
        self.clean_notes()

        print "\nREGION NOTES / BREVES REGIONNALES"
        self._draw_separator()
        self.clean_region_notes()
        
        print "\nVOYAGES / ARTICLES VOYAGES"
        self._draw_separator()
        self.clean_voyages()

    
    def clean_anger(self):
        print "Nothing yet..."
        
    
    def clean_articles(self):
        print "Nothing yet..."
        

    def clean_epicurien(self):
        """
        Clean articles of "Epicurien" category.
        
        """
        from critica.apps.categories.models import Category
        from critica.apps.epicurien.models import EpicurienArticleType
        from critica.apps.epicurien.models import EpicurienArticle
        
        # Delete empty articles
        # ----------------------------------------------------------------------
        try:
            articles = EpicurienArticle.objects.filter(title__contains='titre indisponible')
            for article in articles:
                article.delete()
        except:
            pass
        print "Delete empty articles... OK.\n"
        
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
        print "Update 'Cote bar' type... OK.\n"
        
        articles_gourmets = EpicurienArticle.objects.filter(category__id=4013)
        for article in articles_gourmets:
            article.type = type_cotegourmets
            article.save()
        print "Update 'Cote Gourmets' type... OK.\n"
            
        articles_fumeurs = EpicurienArticle.objects.filter(category__id=4012)
        for article in articles_fumeurs:
            article.type = type_cotefumeurs
            article.save()
        print "Update 'Cote fumeurs' type... OK.\n"
        
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
        print "Nothing yet..."


    def clean_notes(self):
        """
        Clean notes.
        
        """
        print "Nothing yet..."


    def clean_region_notes(self):
        """
        Clean region notes.
        
        """
        print "Nothing yet..."


    def clean_voyages(self):
        """
        Clean articles of "Voyages" category.
        
        """
        from critica.apps.voyages.models import VoyagesArticle    
        self._regroup_issues(VoyagesArticle)

     
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
                display_issues = []
                for i in item.issues.all():
                    display_issues.append(int(i.number))
                print "%s: %s" % (item.title, display_issues)
                changed = True
        print "\nRegroup issues... OK.\n"
        items = model.objects.all()
        for item in items:
            if len(item.issues.all()) < 2:
                item.delete()
        print "Delete extra articles... OK.\n"


