# -*- coding: utf-8 -*-
"""
Tests of ``critica.apps.front`` application.

"""
from django.test import TestCase
from django.core.urlresolvers import reverse


class EmptyFrontTestCase(TestCase):
    """
    Empty front test case.
    
    """
    def test_front_home(self):
        """
        Tests front homepage.
        
        """
        # Should return 404
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 404)


    def test_front_category(self):
        """
        Tests front category.
        
        """
        from critica.apps.categories.models import Category
        # Unstandard categories has to be removed
        EXCLUDED_CATEGORIES = ['coup-de-gueule', 'epicurien', 'voyages', 'regions']
        categories = Category.objects.exclude(slug__in=EXCLUDED_CATEGORIES)
        # Iterates categories
        for category in categories:
            # Should return 404
            response = self.client.get(reverse('category', args=[category.slug]))
            self.assertEqual(response.status_code, 404)


    def test_front_regions(self):
        """
        Tests front Regions category.
        
        """
        # Should return 404
        response = self.client.get(reverse('category_regions'))
        self.assertEqual(response.status_code, 404)


    def test_front_voyages(self):
        """
        Tests front Voyages category.
        
        """
        # Should return 404
        response = self.client.get(reverse('category_voyages'))
        self.assertEqual(response.status_code, 404)


    def test_front_epicurien(self):
        """
        Tests front Epicurien category.
        
        """
        # Should return 404
        response = self.client.get(reverse('category_epicurien'))
        self.assertEqual(response.status_code, 404)


    def test_front_anger(self):
        """
        Tests front Anger category.
        
        """
        # Should return 404
        response = self.client.get(reverse('category_anger'))
        self.assertEqual(response.status_code, 404)



class FrontTestCase(TestCase):
    """
    Front application test case.
    
    """
    fixtures = ['sample_data']
    
    
    def test_front_home(self):
        """
        Tests front homepage.
        
        """
        # Please baby, return 200
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Checks if template is the good one and if we are in the current mode
        self.assertTemplateUsed(response, 'front/home.html')
        self.assertEqual(response.context[0]['is_current'], True)
        self.assertEqual(response.context[0]['is_preview'], False)
        self.assertEqual(response.context[0]['is_archive'], False)
        # Gets current issue object
        # Populated by critica.context_processors.current_issue
        current_issue = response.context[0]['current_issue']
        self.assert_(current_issue)
        # 9 articles
        from critica.apps.articles.models import Article
        EXCLUDED_CATEGORIES = ['coup-de-gueule', 'voyages', 'epicurien', 'regions']
        articles_count = Article.published.filter(issues__id=current_issue.id).exclude(category__slug__in=EXCLUDED_CATEGORIES).count()
        self.assertEqual(articles_count, 9)
        # 1 region note
        self.assert_(response.context[0]['region_note'])
        self.assertEqual(hasattr(response.context[0]['region_note'], '__iter__'), False)
        # 1 anger article
        self.assert_(response.context[0]['anger_article'])
        self.assertEqual(hasattr(response.context[0]['anger_article'], '__iter__'), False)
        # 1 voyages article
        self.assert_(response.context[0]['voyages_article'])
        self.assertEqual(hasattr(response.context[0]['voyages_article'], '__iter__'), False)
        # 3 epicurien articles
        self.assert_(response.context[0]['epicurien_articles'])
        self.assertEqual(len(response.context[0]['epicurien_articles']), 3)
        # 1 illustration of the day
        from critica.apps.illustrations.models import IllustrationOfTheDay
        self.assert_(response.context[0]['illustration'])
        self.assertEqual(hasattr(response.context[0]['illustration'], '__iter__'), False)
        # 1 video
        from critica.apps.videos.models import Video
        self.assert_(response.context[0]['video'])
        self.assertEqual(hasattr(response.context[0]['illustration'], '__iter__'), False)
        
        
    def test_front_category(self):
        """
        Tests front category.
        
        """
        from critica.apps.categories.models import Category
        from critica.apps.notes.models import Note
        from critica.apps.articles.models import Article
        # Unstandard categories has to be removed
        EXCLUDED_CATEGORIES = ['coup-de-gueule', 'epicurien', 'voyages', 'regions']
        categories = Category.objects.exclude(slug__in=EXCLUDED_CATEGORIES)
        # Iterates categories
        for category in categories:
            # Should return 200
            response = self.client.get(reverse('category', args=[category.slug]))
            self.assertEqual(response.status_code, 200)
            # Gets current issue object
            # Populated by critica.context_processors.current_issue
            current_issue = response.context[0]['current_issue']
            self.assert_(current_issue)
            # Should use the good template and we must be in the current mode
            self.assertTemplateUsed(response, 'front/category.html')
            self.assertEqual(response.context[0]['is_current'], True)
            self.assertEqual(response.context[0]['is_preview'], False)
            self.assertEqual(response.context[0]['is_archive'], False)
            # 1 article
            article = Article.published.get(issues__id=current_issue.id, category=category)
            self.assert_(response.context[0]['article'])
            self.assertEqual(hasattr(response.context[0]['article'], '__iter__'), False)
            # 10 notes
            notes_count = Note.published.filter(issues__id=current_issue.id, category=category).count()
            self.assertEqual(notes_count, 10)
            

    def test_front_regions(self):
        """
        Tests front Regions category.
        
        """
        # Should return 200
        response = self.client.get(reverse('category_regions'))
        self.assertEqual(response.status_code, 200)
        # Gets current issue object
        # Populated by critica.context_processors.current_issue
        current_issue = response.context[0]['current_issue']
        self.assert_(current_issue)
        # Should use the good template and we must be in the current mode
        self.assertTemplateUsed(response, 'front/regions.html')
        self.assertEqual(response.context[0]['is_current'], True)
        self.assertEqual(response.context[0]['is_preview'], False)
        self.assertEqual(response.context[0]['is_archive'], False) 
        # 26 region notes
        from critica.apps.regions.models import RegionNote
        region_notes = RegionNote.published.filter(issues__id=current_issue.id).count()
        self.assertEqual(region_notes, 26)
        # 1 featured region note
        self.assert_(response.context[0]['featured_region_note'])
        self.assertEqual(hasattr(response.context[0]['featured_region_note'], '__iter__'), False)

        
    def test_front_voyages(self):
        """
        Tests front Voyages category.
        
        """
        # Should return 200
        response = self.client.get(reverse('category_voyages'))
        self.assertEqual(response.status_code, 200)
        # Should use the good template and we must be in the current mode
        self.assertTemplateUsed(response, 'front/voyages.html')
        self.assertEqual(response.context[0]['is_current'], True)
        self.assertEqual(response.context[0]['is_preview'], False)
        self.assertEqual(response.context[0]['is_archive'], False) 
        # 1 article
        self.assert_(response.context[0]['article'])
        self.assertEqual(hasattr(response.context[0]['article'], '__iter__'), False)
        # Archives
        self.assert_(response.context[0]['archives'])
        # 10 archives max.
        over_max_archives = False
        if len(response.context[0]['archives']) > 10:
            over_max_archives = True
        else:
            over_max_archives = False
        self.assertFalse(over_max_archives)


    def test_front_epicurien(self):
        """
        Tests front Epicurien category.
        
        """
        # Should return 200
        response = self.client.get(reverse('category_epicurien'))
        self.assertEqual(response.status_code, 200)
        # Should use the good template and we must be in the current mode
        self.assertTemplateUsed(response, 'front/epicurien.html')
        self.assertEqual(response.context[0]['is_current'], True)
        self.assertEqual(response.context[0]['is_preview'], False)
        self.assertEqual(response.context[0]['is_archive'], False)
        # 3 articles: article_cotefumeurs, article_cotegourmets and article_cotebar
        self.assert_(response.context[0]['article_cotefumeurs'])
        self.assertEqual(hasattr(response.context[0]['article_cotefumeurs'], '__iter__'), False)
        self.assert_(response.context[0]['article_cotegourmets'])
        self.assertEqual(hasattr(response.context[0]['article_cotegourmets'], '__iter__'), False)
        self.assert_(response.context[0]['article_cotebar'])
        self.assertEqual(hasattr(response.context[0]['article_cotebar'], '__iter__'), False)
        # Archives
        over_max_archives = False
        # Archives cote fumeurs (max 10)
        self.assert_(response.context[0]['archives_cotefumeurs'])
        if len(response.context[0]['archives_cotefumeurs']) > 10:
            over_max_archives = True
        else:
            over_max_archives = False
        self.assertFalse(over_max_archives)
        # Archives cote gourmets (max 10)
        self.assert_(response.context[0]['archives_cotegourmets'])
        if len(response.context[0]['archives_cotegourmets']) > 10:
            over_max_archives = True
        else:
            over_max_archives = False
        self.assertFalse(over_max_archives)
        # Archives cote bar (max 10)
        self.assert_(response.context[0]['archives_cotebar'])
        if len(response.context[0]['archives_cotebar']) > 10:
            over_max_archives = True
        else:
            over_max_archives = False
        self.assertFalse(over_max_archives)


    def test_front_anger(self):
        """
        Tests front Anger category.
        
        """
        # Should return 200
        response = self.client.get(reverse('category_anger'))
        self.assertEqual(response.status_code, 200)
        # Should use the good template and we must be in the current mode
        self.assertTemplateUsed(response, 'front/anger.html')
        self.assertEqual(response.context[0]['is_current'], True)
        self.assertEqual(response.context[0]['is_preview'], False)
        self.assertEqual(response.context[0]['is_archive'], False) 
        # 1 article
        self.assert_(response.context[0]['article'])
        self.assertEqual(hasattr(response.context[0]['article'], '__iter__'), False)
        # Archives (max 10)
        self.assert_(response.context[0]['archives'])
        if len(response.context[0]['archives']) > 10:
            over_max_archives = True
        else:
            over_max_archives = False
        self.assertFalse(over_max_archives)



