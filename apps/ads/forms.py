# -*- coding utf-8 -*-
"""
Ads application custom forms.

"""
import os
from PIL import Image
import hexagonit.swfheader
from StringIO import StringIO  
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms.util import ErrorList
from critica.apps.ads.models import AdDefaultBanner
from critica.apps.ads.models import AdBanner
from critica.apps.ads.models import AdBannerPosition


class CustomBannerForm(forms.ModelForm):
    """
    Custom banner form.
    
    """
    class Meta:
        abstract = True
        
    def clean(self):
        # Cleaned datas
        if self.cleaned_data.has_key('banner'):
            banner = self.cleaned_data['banner']
            
        if self.cleaned_data.has_key('positions'):
            positions = self.cleaned_data['positions']
        
        if self.cleaned_data.has_key('starting_date'):
            starting_date = self.cleaned_data['starting_date']
            
        if self.cleaned_data.has_key('ending_date'):
            ending_date = self.cleaned_data['ending_date']
            
        # Extensions
        file_exts = ('.png', '.jpg', '.jpeg', '.gif', '.swf')
        image_exts = ('.png', '.jpg', '.jpeg', '.gif')
        
        # Check banner extension
        is_valid_extension = True
        from os.path import splitext
        if splitext(banner.name)[1].lower() not in file_exts:
            msg = _('Sorry, only these file types are supported: .png, .jpg, .jpeg, .gif and .swf. Please, upload a new one.')
            self._errors['banner'] = ErrorList([msg])
            is_valid_extension = False
        is_image = False
        if splitext(banner.name)[1].lower() in image_exts:
            is_image = True
            
        # Check image / swf format
        if positions and is_valid_extension:
            position = positions[0]
            format_width = position.format.width
            format_height = position.format.height
            if hasattr(banner, 'temporary_file_path'):
                file = banner.temporary_file_path()
            else:
                if hasattr(banner, 'read'):
                    file = StringIO(banner.read())
                else:
                    file = banner
            if is_image:
                trial_image = Image.open(file)
                banner_width, banner_height = trial_image.size
            else:
                trial_image = hexagonit.swfheader.parse(file)
                banner_width = trial_image['width']
                banner_height = trial_image['height']
            if banner_width != format_width and banner_height != format_height:
                msg = _('Please, upload an image or a swf file in the correct format.')
                self._errors['banner'] = ErrorList([msg])
        
        return self.cleaned_data


class CustomAdBannerForm(CustomBannerForm):
    """
    Custom form of AdBanner model.
    
    """
    class Meta:
        model = AdBanner


class CustomAdDefaultBannerForm(CustomBannerForm):
    """
    Custom form of AdDefaultBanner model.
    
    """
    class Meta:
        model = AdDefaultBanner
    




        

