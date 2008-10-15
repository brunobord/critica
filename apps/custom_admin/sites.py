# -*- coding: utf-8 -*-
"""
Custom Admin sites.

"""
from datetime import datetime
from django.contrib.admin.sites import AdminSite
from django import http, template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Custom admin
# ------------------------------------------------------------------------------
class CustomAdminSite(AdminSite):
    """
    An AdminSite object encapsulates an instance of the Django admin application, ready
    to be hooked in to your URLConf. Models are registered with the AdminSite using the
    register() method, and the root() method can then be used as a Django view function
    that presents a full admin interface for the collection of registered models.
    
    CustomAdminSite is a basic Django admin.
    
    """
    index_template = 'custom_admin/index.html'


# Sites
# ------------------------------------------------------------------------------
custom_site = CustomAdminSite()


# Default registers
# ------------------------------------------------------------------------------
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

custom_site.register(User, UserAdmin)
custom_site.register(Group, GroupAdmin)

from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

custom_site.register(Site, SiteAdmin)
