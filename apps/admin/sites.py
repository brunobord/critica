# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.admin.sites import AdminSite
from django import http, template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache


# Basic admin
# ------------------------------------------------------------------------------
class BasicAdminSite(AdminSite):
    """
    An AdminSite object encapsulates an instance of the Django admin application, ready
    to be hooked in to your URLConf. Models are registered with the AdminSite using the
    register() method, and the root() method can then be used as a Django view function
    that presents a full admin interface for the collection of registered models.
    
    BasicAdminSite is a basic Django admin with lightweight customizations.
    
    """
    index_template = 'basic_admin/index.html'


    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        
        """
        context = {
            'title': _('Site administration'),
            'root_path': self.root_path,
        }
        context.update(extra_context or {})
        return render_to_response(self.index_template or 'admin/index.html', context,
            context_instance=template.RequestContext(request)
        )
    index = never_cache(index)

    def dashboard_index(self, request):
        """
        Basic admin dashboard view.
        
        """
        from critica.apps.articles.models import Article
        from critica.apps.notes.models import Note
        articles = Article.objects.all()
        notes = Note.objects.all()
        return render_to_response(
            'basic_admin/current_issue/dashboard/index.html', 
            {'articles': articles, 'notes': notes}, 
            context_instance=RequestContext(request)
        )

# Advanced admin
# ------------------------------------------------------------------------------    
class AdvancedAdminSite(AdminSite):
    """
    An AdminSite object encapsulates an instance of the Django admin application, ready
    to be hooked in to your URLConf. Models are registered with the AdminSite using the
    register() method, and the root() method can then be used as a Django view function
    that presents a full admin interface for the collection of registered models.
    
    AdvancedAdminSite is an advanced Django admin with heavy customizations.
    
    """
    index_template = 'advanced_admin/index.html'


# Sites
# ------------------------------------------------------------------------------
basic_site = BasicAdminSite()
advanced_site = AdvancedAdminSite()


# Default registers
# ------------------------------------------------------------------------------
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

basic_site.register(User, UserAdmin)
basic_site.register(Group, GroupAdmin)

advanced_site.register(User, UserAdmin)
advanced_site.register(Group, GroupAdmin)

from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

basic_site.register(Site, SiteAdmin)
advanced_site.register(Site, SiteAdmin)
