# test class
from django.test import TestCase
from critica.apps.positions import settings as position_settings

class SettingsTestCase(TestCase):

    def test_settings(self):
        self.assertTrue(isinstance(position_settings.CATEGORY_DEFAULT_ORDER, list))
        self.assertTrue(len(position_settings.CATEGORY_DEFAULT_ORDER) > 0)
        self.assertTrue(isinstance(position_settings.CATEGORY_DEFAULT_POSITION, dict))
        self.assertTrue(len(position_settings.CATEGORY_DEFAULT_POSITION) > 0)
        

