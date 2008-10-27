# -*- coding: utf-8 -*-
"""
Widgets of ``critica.apps.articles`` application.

"""
from django.forms.widgets import FileInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext


class ImageWithThumbWidget(FileInput):
    """
    Custom image field widget that displays image thumbnail.
    
    """
    def __init__(self, thumb_width=80):
        self.width = thumb_width
        super(ImageWithThumbWidget, self).__init__({})

    def render(self, name, value, attrs=None):
        thumb_html = ''
        title = ugettext('current image')
        if value and hasattr(value, "url"):
            thumb_html = '<p style="line-height: 2.1em;"><span style="font-size:1.1em; font-weight: bold; font-variant:small-caps;">%s</span><br /><img src="%s" width="%s" style="border: 2px solid #000; " /><br /><strong><a href="%s">%s</a></strong></p>' % (title, value.url, self.width, value.url, value)
        return mark_safe("%s %s" % (super(ImageWithThumbWidget, self).render(name, value, attrs), thumb_html))

