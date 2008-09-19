# -*- coding: utf-8 -*-
from django.contrib.admin.sites import AdminSite


# Basic admin
# ------------------------------------------------------------------------------
class BasicAdminSite(AdminSite):
    pass
    

# Advanced admin
# ------------------------------------------------------------------------------    
class AdvancedAdminSite(AdminSite):
    pass


# Sites
# ------------------------------------------------------------------------------
basic_site = BasicAdminSite()
advanced_site = AdvancedAdminSite()
