"""
Feeds for ``critica``.

"""
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Rss201rev2Feed, Atom1Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from critica.apps.journal.models import Article, Category


class RssArticles(Feed):
    """ RSS feed: latest articles. """
    feed_type = Rss201rev2Feed
    title_template = 'feeds/item_title.html'
    description_template = 'feeds/item_description.html'
    
    def title(self):
        _site = Site.objects.get_current()
        return _('%(site_name)s: latest articles feed') % {
            'site_name': _site.name,
        }

    def link(self):
        return reverse('home')
        
    def description(self):
        _site = Site.objects.get_current()
        return _('Recent articles published on %(site_name)s.') % {
            'site_name': _site.name,
        }
        
    def items(self):
        return Article.complete.all().order_by('-publication_date')

    def item_pubdate(self, obj):
        return obj.publication_date



class RssArticlesByCategory(RssArticles):
    """ RSS feed: latest articles published in a given category. """
    
    def get_object(self, bits):
        return Category.objects.get(slug__exact=bits[1])
        
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
        return obj.complete_article_set.all()

    def item_pubdate(self, obj):
        return obj.publication_date



class AtomArticles(RssArticles):
    """ Atom feed: latest articles. """
    feed_type = Atom1Feed
    subtitle = RssArticles.description



class AtomArticlesByCategory(RssArticlesByCategory):
    """ Atom feed: latest articles published in a given category. """
    feed_type = Atom1Feed
    subtitle = RssArticlesByCategory.description


