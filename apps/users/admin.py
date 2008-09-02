# -*- coding: utf-8 -*-
"""
Administration interface options for ``cockatoo.apps.users`` models.

"""
from django.contrib import admin
from critica.apps.users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """ Administration interface options for ``UserProfile`` model. """
    pass
    
#admin.site.register(UserProfile, UserProfileAdmin)

