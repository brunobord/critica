"""
Feeds for ``critica``.

"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Rss201rev2Feed, Atom1Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from critica.apps.articles.models import Article
from critica.apps.voyages.models import VoyagesArticle
from critica.apps.epicurien.models import EpicurienArticle
from critica.apps.anger.models import AngerArticle
from critica.apps.notes.models import Note
from critica.apps.regions.models import FeaturedRegion
from critica.apps.regions.models import RegionNote
from critica.apps.categories.models import Category


class LatestRss(Feed):
    """ 
    Homepage RSS feed.
    
    """
    feed_type            = Rss201rev2Feed
    title_template       = 'syndication/feeds/item_title.html'
    description_template = 'syndication/feeds/item_description.html'
    
    def title(self):
        """
        Channel title.
        
        """
        _site = Site.objects.get_current()
        return _('%(site_name)s: latest articles feed') % {
            'site_name': _site.name,
        }

    def link(self):
        """
        Channel link.
        
        """
        return reverse('home')
        
    def description(self):
        """
        Channel description.
        
        """
        _site = Site.objects.get_current()
        return _('Recent articles and notes published on %(site_name)s.') % {
            'site_name': _site.name,
        }
        
    def items(self):
        """
        Channel items.        

        """
        all_items = []
        # Articles standard categories
        articles = Article.published.order_by('-publication_date')[0:9]
        for a in articles:
            all_items.append((a.id, a))
        # Regions
        featured = FeaturedRegion.objects.filter(issue__is_published=True).order_by('-issue')[0:1].get()
        region_note = RegionNote.published.get(region=featured.region.id)
        all_items.append((region_note.id, region_note))
        # Voyages
        article_voyages = VoyagesArticle.published.order_by('-publication_date')[0:1].get()
        all_items.append((article_voyages.id, article_voyages))
        # Epicurien
        articles_epicurien = EpicurienArticle.published.order_by('-publication_date')[0:3]
        for a in articles_epicurien:
            all_items.append((a.id, a))
        # Anger
        article_anger = AngerArticle.published.order_by('-publication_date')[0:1].get()
        all_items.append((article_anger.id, article_anger))
        items = [item for k, item in all_items]
        return items

    def item_link(self, obj):
        """
        Channel item link.
        
        """
        return obj.get_archive_url()


class LatestByCategoryRss(LatestRss):
    """ 
    RSS feed: latest articles published in a given category. 
    
    """
    title_template       = 'syndication/feeds/category_item_title.html'
    description_template = 'syndication/feeds/category_item_description.html'
    
    def get_object(self, bits):
        """
        Get category.
        
        """
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])
        
    def title(self, obj):
        """
        Channel title.
        
        """
        _site = Site.objects.get_current()
        return _('%(site_name)s: "%(category)s" category feed') % {
            'site_name': _site.name, 
            'category': obj.name,
        }

    def description(self, obj):
        """
        Channel description.
        
        """
        _site = Site.objects.get_current()
        description = _('Recent articles published in the category "%(category)s" on %(site_name)s.') % {'category': obj.name, 'site_name': _site.name}
        return description
           
    def link(self, obj):
        """
        Channel link.
        
        """
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
        
    def items(self, obj):
        """
        Channel items.
        
        """
        if obj.slug == 'voyages':
            return VoyagesArticle.published.order_by('-publication_date')[0:1]
        elif obj.slug == 'epicurien':
            return EpicurienArticle.published.order_by('-publication_date')[0:3]
        elif obj.slug == 'coup-de-gueule':
            return AngerArticle.published.order_by('-publication_date')[0:1]
        elif obj.slug == 'regions':
            return RegionNote.published.order_by('-publication_date')[0:26]
        else:
            all_items = []
            # Article
            article = Article.published.filter(category=obj).order_by('-publication_date')[0:1].get()
            all_items.append((article.id, article))
            # Notes
            notes = Note.published.filter(category=obj).order_by('-publication_date')[0:40]
            for note in notes:
                all_items.append((note.id, note))
            items = [item for k, item in all_items]
            return items
            
    def item_link(self, obj):
        """
        Channel item link.
        
        """
        return obj.get_archive_url()

