# -*- coding: utf-8 -*-
""""
Tests of ``critica.apps.quotas`` application.

"""
import datetime
from django.test import TestCase
from critica.apps.quotas.models import DefaultCategoryQuota
from critica.apps.quotas.models import CategoryQuota
from critica.apps.issues.models import Issue
from critica.apps.categories.models import Category
from MySQLdb import IntegrityError


class DefaultCategoryQuotaTestCase(TestCase):
    """
    Default category quota test case.
    
    """
    def test_default_category_quota(self):
        """
        Tests default category quota.
        
        """
        # national
        category = Category.objects.get(slug='national')
        quota = DefaultCategoryQuota.objects.get(category=category)
        self.assertEquals(quota.quota, 11)
        # epicurien
        category = Category.objects.get(slug='epicurien')
        quota = DefaultCategoryQuota.objects.get(category=category)
        self.assertEquals(quota.quota, 3)

    def test_unique_category(self):
        """
        Tests unique category (a category must be unique).
        
        """
        category = Category.objects.get(slug='national')
        default_quota = DefaultCategoryQuota(category=category, quota=11)
        self.assertRaises(IntegrityError, default_quota.save)


class CategoryQuotaTestCase(TestCase):
    """
    Category quota test case.
    
    """
    def test_issue_category_quotas(self):
        """
        Tests issue category quotas.
        
        """
        # Creates an issue.
        issue = Issue(number=10, publication_date=datetime.date.today(), status=1)
        issue.save()
        # Gets quotas for this issue and checks if quotas have been created for each category.
        quotas_for_issue = CategoryQuota.objects.filter(issue=issue)
        count_categories = Category.objects.count()
        count_quotas = quotas_for_issue.count()
        self.assertEquals(count_categories, count_quotas)
        # Tests default category quotas
        for quota in quotas_for_issue:
            default_quota = DefaultCategoryQuota.objects.get(category=quota.category)
            self.assertEquals(default_quota.quota, quota.quota)


