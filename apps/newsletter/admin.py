# -*- coding: utf-8 -*-
""" 
Administration interface options of ``critica.apps.newsletter`` models. 

"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from critica.apps.custom_admin.sites import custom_site
from critica.apps.newsletter.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Newsletter`` model.
    
    """
    list_display = ('ald_subscriber', 'email', 'zip_code')
    list_filter = ['zip_code']
    ordering = ['first_name', 'last_name']


    def ald_subscriber(self, obj):
        """
        Formatted subscriber for admin list_display option.
        
        """
        return u'%s %s' % (obj.first_name, obj.last_name)
    ald_subscriber.short_description = _('subscriber')
    

admin.site.register(Subscriber, SubscriberAdmin)
custom_site.register(Subscriber, SubscriberAdmin)
