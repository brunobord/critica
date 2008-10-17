# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ObjectDoesNotExist
from critica.apps.articles.models import Article
from tagging.models import TaggedItem


register = template.Library()


@register.inclusion_tag('front/includes/related_articles.html')
def display_related_articles(obj):
    # Articles tags
    article_tags = obj.tags
    # Articles from the same category
    category_articles = Article.objects.filter(category=obj.category, is_ready_to_publish=True, is_reserved=False).exclude(id=obj.id)
    # Articles from the same category tagged with the same tags
    articles = TaggedItem.objects.get_union_by_model(category_articles , article_tags)
    # Related articles
    related_articles = articles[:3]
    return {'related_articles': related_articles}

