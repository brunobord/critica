#!/usr/bin/env python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from critica.apps.newsletter.utils import sender

if __name__ == "__main__":
    sender.subscriber_loop()
