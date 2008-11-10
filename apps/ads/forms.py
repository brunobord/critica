# -*- coding utf-8 -*-
"""
Ads application custom forms.

"""
import os
import datetime
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
from critica.apps.ads.models import AdCarousel
from critica.apps.ads.models import AdCarouselBanner
from critica.lib.widgets import ImageWithThumbWidget


class CustomBannerForm(forms.ModelForm):
    """
    Custom banner form.
    
    """
    class Meta:
        abstract = True
        
    def clean(self):
        """
        Form validation process.
        
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
        if self.cleaned_data['starting_date'] and self.cleaned_data['ending_date'] and self.cleaned_data['positions']:
            # Get proposed positions
            proposed_positions = []
            for p in self.cleaned_data['positions']:
                proposed_positions.append(p.id)
                
            # Get proposed dates
            proposed_dates = []
            for day in xrange((self.cleaned_data['ending_date'] - self.cleaned_data['starting_date']).days + 1):
                proposed_dates.append(self.cleaned_data['starting_date'] + datetime.timedelta(day))

            # Get existing banners with same positions and starting date / ending date in proposed dates
            existing_banners = AdBanner.objects.filter(positions__id__in=proposed_positions)
            if hasattr(self.instance, 'id'):
                existing_banners = existing_banners.exclude(pk=self.instance.id)
            
            # Check positions and dates
            for existing_banner in existing_banners:
                for existing_banner_position in existing_banner.positions.all():
                    for proposed_position in proposed_positions:
                        if proposed_position == existing_banner_position.id:
                            existing_banner_dates = []
                            for day in xrange((existing_banner.ending_date - existing_banner.starting_date).days + 1):
                                existing_banner_dates.append(existing_banner.starting_date + datetime.timedelta(day))
                            common_dates = [d for d in proposed_dates if d in existing_banner_dates]
                            if common_dates:
                                msg = _('Date already taken. Please, select another. Taken dates for this position: %(dates)s') % {
                                    'dates': ', '.join([d.strftime('%Y/%m/%d') for d in common_dates]),
                                }
                                self._errors['starting_date'] = ErrorList([msg])
                                self._errors['ending_date'] = ErrorList([msg])
        
        # Return
        # -----------------------------------------------------------------------
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
    

class AdCarouselAdminForm(forms.ModelForm):
    """
    Custom form of ``AdCarousel`` model.
    
    """
    class Meta:
        model = AdCarousel
        
    def clean(self):
        """
        Form validation process.
        
        """
        # Validation of dates
        # ----------------------------------------------------------------------
        if self.cleaned_data['starting_date'] and self.cleaned_data['ending_date'] and self.cleaned_data['positions']:
            # Get proposed positions
            proposed_positions = []
            for p in self.cleaned_data['positions']:
                proposed_positions.append(p.id)
                
            # Get proposed dates
            proposed_dates = []
            for day in xrange((self.cleaned_data['ending_date'] - self.cleaned_data['starting_date']).days + 1):
                proposed_dates.append(self.cleaned_data['starting_date'] + datetime.timedelta(day))

            # Get existing banners with same positions and starting date / ending date in proposed dates
            existing_carousels = AdCarousel.objects.filter(positions__id__in=proposed_positions)
            if hasattr(self.instance, 'id'):
                existing_carousels = existing_carousels.exclude(pk=self.instance.id)
            
            # Check positions and dates
            for existing_carousel in existing_carousels:
                for existing_carousel_position in existing_carousel.positions.all():
                    for proposed_position in proposed_positions:
                        if proposed_position == existing_carousel_position.id:
                            existing_carousel_dates = []
                            for day in xrange((existing_carousel.ending_date - existing_carousel.starting_date).days + 1):
                                existing_carousel_dates.append(existing_carousel.starting_date + datetime.timedelta(day))
                            common_dates = [d for d in proposed_dates if d in existing_carousel_dates]
                            if common_dates:
                                msg = _('Date already taken. Please, select another. Taken dates for this position: %(dates)s') % {
                                    'dates': ', '.join([d.strftime('%Y/%m/%d') for d in common_dates]),
                                }
                                self._errors['starting_date'] = ErrorList([msg])
                                self._errors['ending_date'] = ErrorList([msg])
        return self.cleaned_data


class AdCarouselBannerAdminForm(forms.ModelForm):
    """
    Custom form of ``AdCarouselBanner`` model.
    
    """
    banner = forms.ImageField(widget=ImageWithThumbWidget, label=_('banner'), help_text=_('Please, select a banner to upload.'))
    
    class Meta:
        model = AdCarouselBanner




