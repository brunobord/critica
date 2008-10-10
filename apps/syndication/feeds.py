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
from critica.apps.regions.models import RegionNote
from critica.apps.categories.models import Category


class LatestRss(Feed):
    """ 
    RSS feed of latest articles / notes.
    
    """
    feed_type = Rss201rev2Feed
    title_template = 'front/feeds/item_title.html'
    description_template = 'front/feeds/item_description.html'
    
    def title(self):
        _site = Site.objects.get_current()
        return _('%(site_name)s: latest articles feed') % {
            'site_name': _site.name,
        }

    def link(self):
        return reverse('home')
        
    def description(self):
        _site = Site.objects.get_current()
        return _('Recent articles and notes published on %(site_name)s.') % {
            'site_name': _site.name,
        }
        
    def items(self):
        all_items = []
        
        # Articles standard categories
        articles = Article.objects.filter(
            issues__is_published=True,
            is_ready_to_publish=True,
            is_reserved=False)[:9]
        for a in articles:
            all_items.append((a.id, a))
        
        # Voyages
        articles_voyages = VoyagesArticle.objects.filter(
            issues__is_published=True,
            is_ready_to_publish=True,
            is_reserved=False)[:1]
        for a in articles_voyages:
            all_items.append((a.id, a))
            
        # Epicurien
        articles_epicurien = EpicurienArticle.objects.filter(
            issues__is_published=True,
            is_ready_to_publish=True,
            is_reserved=False)[:3]
        for a in articles_epicurien:
            all_items.append((a.id, a))
            
        # Anger
        articles_anger = AngerArticle.objects.filter(
            issues__is_published=True,
            is_ready_to_publish=True,
            is_reserved=False)[:1]
        for a in articles_anger:
            all_items.append((a.id, a))
        
        items = [item for k, item in all_items]
        
        return items



class LatestByCategoryRss(LatestRss):
    """ RSS feed: latest articles published in a given category. """
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])
        
    def title(self, obj):
        _site = Site.objects.get_current()
        return _('%(site_name)s: "%(category)s" category feed') % {
            'site_name': _site.name, 
            'category': obj.name,
        }

    def description(self, obj):
        _site = Site.objects.get_current()
        description = _('Recent articles published in the category "%(category)s" on %(site_name)s.') % {'category': obj.name, 'site_name': _site.name}
        return description
           
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
        
    def items(self, obj):
        return obj.complete_article_set.all()[:10]

    def item_pubdate(self, obj):
        return obj.publication_date


