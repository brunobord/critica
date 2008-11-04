# -*- coding: utf-8 -*-
"""
Managers of ``critica.apps.ads`` application.

"""
from django.db import models


class AdBannerManager(models.Manager):
    """
    Manager of ``AdBanner`` model.
    
    """
    def _get_obj_dates(self, start, end):
        import datetime
        dates = []
        for day in xrange((end - start).days):
            dates.append(start + datetime.timedelta(day))
        return dates
        
    def get_taken_dates(self):
        banners = self.all()
        dates = []
        for banner in banners:
            dates = [date for date in self._get_obj_dates(banner.starting_date, banner.ending_date)]
        return dates
            
    
