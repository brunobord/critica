import datetime
from django.test import TestCase
from apps.issues.models import Issue
from apps.positions.models import CategoryPosition
from apps.categories.models import Category
from apps.positions import settings as positions_settings


class IssueTestCase(TestCase):

    def test_create_issue(self):
        issue = Issue(number=100, publication_date=datetime.date.today())
        issue.save()
        # check the category position
        for slug in positions_settings.CATEGORY_DEFAULT_ORDER:
            category = Category.objects.get(slug=slug)
            positions = CategoryPosition.objects.filter(issue=issue, category=category)
            self.assertEquals(len(positions), 1)
            if slug in positions_settings.CATEGORY_DEFAULT_POSITION:
                self.assertEquals(positions[0].position, positions_settings.CATEGORY_DEFAULT_POSITION[slug])
