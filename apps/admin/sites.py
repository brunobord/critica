# -*- coding: utf-8 -*-
from django.contrib.admin.sites import AdminSite
from django import http, template
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime


# Basic admin
# ------------------------------------------------------------------------------
class BasicAdminSite(AdminSite):
    index_template = 'basic_admin/index.html'
    
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
