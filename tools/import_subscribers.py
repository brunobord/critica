#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
An ugly script to import existing newsletter subscribers into dabatase.

"""
PROJECT_PATH = '/home/gilles/Work/dev/critica/branches/trunk'
PROJECT_SETTINGS_MODULE = 'critica.settings'


import datetime, time
import sys
sys.path.append(PROJECT_PATH)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_SETTINGS_MODULE
import csv
from critica.apps.newsletter.models import Subscriber


def main():
    args = sys.argv[1:]
    filename = args[0]
    cr = csv.reader(open(filename, 'rb'), delimiter=';')
    all_subscribers = []
    for row in cr:
        all_subscribers.append(row[0])
    subscribers = list(set(all_subscribers))
    for sub in subscribers:
        subscriber = Subscriber(email=sub[0])
        subscriber.save()
     
if __name__ == '__main__':
    main()
