# -*- coding: utf-8 -*-
"""
Administration interface options of ``critica.apps.users`` models.

"""
from django.contrib import admin
from critica.apps.users.models import UserProfile
from critica.apps.users.models import UserNickname
from critica.apps.custom_admin.sites import custom_site


class UserProfileAdmin(admin.ModelAdmin):
    """ 
    Administration interface options of ``UserProfile`` model. 
    
    """
    pass


class UserNicknameAdmin(admin.ModelAdmin):
    """
    Administration interface of ``UserNickname`` model.
    
    """
    list_display  = ('user', 'nickname')
    list_filter   = ('user',)
    search_fields = ('user', 'nickname')
    ordering      = ['user']


# Registers
# ------------------------------------------------------------------------------
admin.site.register(UserProfile, UserProfileAdmin)
custom_site.register(UserProfile, UserProfileAdmin)

admin.site.register(UserNickname, UserNicknameAdmin)
custom_site.register(UserNickname, UserNicknameAdmin)
