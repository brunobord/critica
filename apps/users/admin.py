# -*- coding: utf-8 -*-
"""
Administration interface options of ``critica.apps.users`` models.

"""
from django.contrib import admin
from critica.apps.users.models import UserProfile, UserNickname
from critica.apps.custom_admin.sites import custom_site


class UserProfileAdmin(admin.ModelAdmin):
    """ 
    Administration interface options of ``UserProfile`` model. 
    
    """
    pass

admin.site.register(UserProfile, UserProfileAdmin)
custom_site.register(UserProfile, UserProfileAdmin)


class UserNicknameAdmin(admin.ModelAdmin):
    """
    Administration interface of ``UserNickname`` model.
    
    """
    list_display = ('user', 'nickname')
    list_filter = ('user',)
    search_fields = ('user', 'nickname')
    ordering = ['user']
    
admin.site.register(UserNickname, UserNicknameAdmin)
custom_site.register(UserNickname, UserNicknameAdmin)
