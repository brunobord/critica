# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.partnerlinks`` application.

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from critica.apps.custom_admin.sites import custom_site
from critica.apps.partnerlinks.models import PartnerLink


class PartnerLinkAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``PartnerLink`` model.
    
    """
    list_display      = ('name', 'ald_link', 'is_active')
    ordering          = ('name',)
    
    def ald_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.link, obj.link)
    ald_link.allow_tags = True
    ald_link.short_description = _('link')


# Registers
# ------------------------------------------------------------------------------
admin.site.register(PartnerLink, PartnerLinkAdmin)
custom_site.register(PartnerLink, PartnerLinkAdmin)
