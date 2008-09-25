# -*- coding: utf-8 -*-
"""
Administration interface options for ``cockatoo.apps.users`` models.

"""
from django.contrib import admin
from critica.apps.users.models import UserProfile, UserNickname
from critica.apps.admin.sites import basic_site, advanced_site


class UserProfileAdmin(admin.ModelAdmin):
    """ 
    Administration interface options for ``UserProfile`` model. 
    
    """
    pass

admin.site.register(UserProfile, UserProfileAdmin)
basic_site.register(UserProfile, UserProfileAdmin)
advanced_site.register(UserProfile, UserProfileAdmin)


class UserNicknameAdmin(admin.ModelAdmin):
    """
    Administration interface for ``UserNickname`` model.
    
    """
    list_display = ('user', 'nickname')
    list_filter = ('user',)
    search_fields = ('user', 'nickname')
    ordering = ('user',)
    
admin.site.register(UserNickname, UserNicknameAdmin)
basic_site.register(UserNickname, UserNicknameAdmin)
advanced_site.register(UserNickname, UserNicknameAdmin)
