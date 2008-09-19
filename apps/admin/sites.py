# -*- coding: utf-8 -*-
from django.contrib.admin.sites import AdminSite


# Basic admin
# ------------------------------------------------------------------------------
class BasicAdminSite(AdminSite):
    index_template = 'basic_admin/index.html'
    

# Advanced admin
# ------------------------------------------------------------------------------    
class AdvancedAdminSite(AdminSite):
    index_template = 'advanced_admin/index.html'


# Sites
# ------------------------------------------------------------------------------
basic_site = BasicAdminSite()
advanced_site = AdvancedAdminSite()
