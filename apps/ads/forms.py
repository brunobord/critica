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
        """
        Form validation process.
        
        Process::
        
            is_valid_extension
                True if extension is OK.
                
            is_valid_position_format
                True if selected format matches the position format.
                
            is_valid_image_format
                True if image format matches the selected format.
                
            is_valid_position_date
                True if position and date are available.
        
        """
        # Cleaned data
        # ----------------------------------------------------------------------
        if self.cleaned_data.has_key('banner'):
            banner = self.cleaned_data['banner']
            
        if self.cleaned_data.has_key('format'):
            format = self.cleaned_data['format']
            
        if self.cleaned_data.has_key('positions'):
            positions = self.cleaned_data['positions']
        
        if self.cleaned_data.has_key('starting_date'):
            starting_date = self.cleaned_data['starting_date']
            
        if self.cleaned_data.has_key('ending_date'):
            ending_date = self.cleaned_data['ending_date']
            
        # Validation of extension
        # ----------------------------------------------------------------------
        is_valid_extension = True
        
        file_exts = ('.png', '.jpg', '.jpeg', '.gif', '.swf')
        image_exts = ('.png', '.jpg', '.jpeg', '.gif')
        
        from os.path import splitext
        if splitext(banner.name)[1].lower() not in file_exts:
            msg = _('Sorry, only these file types are supported: .png, .jpg, .jpeg, .gif and .swf. Please, upload a new one.')
            self._errors['banner'] = ErrorList([msg])
            is_valid_extension = False
        is_image = False
        if splitext(banner.name)[1].lower() in image_exts:
            is_image = True
            
        # Validation of position <=> format
        # ----------------------------------------------------------------------
        is_valid_position_format = True
        
        if positions and is_valid_extension:
            for position in positions:
                if position.format != format:
                    msg = _('Please, only select a position related to the format.')
                    self._errors['positions'] = ErrorList([msg])
                    is_valid_position_format = False
        
        # Validation of real image format
        # ----------------------------------------------------------------------
        is_valid_image_format = True
        
        if is_valid_extension and is_valid_position_format:
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
            
            if banner_width != format.width and banner.height != format_height:
                msg = _('Please, upload an image or a swf file in the correct format.')
                self._errors['banner'] = ErrorList([msg])
                is_valid_image_format = False
                
        # Validation of dates
        # ----------------------------------------------------------------------
        if starting_date and ending_date and positions:
            current_positions = []
            for p in self.cleaned_data['positions']:
                current_positions.append(p.id)
            existing_banners = AdBanner.objects.filter(positions__id__in=current_positions)
            existing_banners = existing_banners.filter(starting_date__lt=starting_date, ending_date__gt=ending_date)
            if existing_banners:
                msg = _('Dates already taken. Please, select other dates.')
                self._errors['starting_date'] = ErrorList([msg])
        
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
    




        

