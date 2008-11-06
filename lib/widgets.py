# -*- coding: utf-8 -*-
"""
Widgets of Critic@ project.

"""
from django import forms
from django.forms.widgets import FileInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.db.models import get_model
from django.utils import simplejson
from tagging.models import Tag


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


class AutoCompleteTagInput(forms.TextInput):
    """
    Auto-complete tag input widget.
    
    """
    class Media:
        css = {
            'all': ('critica/css/jquery.autocomplete.css',)
        }
        js = (
            'critica/js/lib/jquery-1.2.6.min.js',
            'critica/js/plugins/jquery.bgiframe.min.js',
            'critica/js/plugins/jquery.ajaxQueue.js',
            'critica/js/plugins/thickbox-compressed.js',
            'critica/js/plugins/jquery.autocomplete.js'
        )
    
    def __init__(self, model=None, attrs=None):
        self.model = get_model(*model.split('.'))
        if attrs:
            self.attrs.update(attrs)
        super(AutoCompleteTagInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        page_tags = Tag.objects.usage_for_model(self.model)
        tag_list = simplejson.dumps([tag.name for tag in page_tags], ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, tag_list))

