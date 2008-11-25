#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple script that dumps given MySQL tables.

"""
import os


# Configuration
# ------------------------------------------------------------------------------
db_name = 'critica'
db_user = 'root'
options = '-e -t'
tables = [
    'anger_article',
    'anger_article_issues',
    'articles_article',
    'articles_article_issues',
    'epicurien_article',
    'epicurien_article_issues',
    'illustrations_illustrationoftheday',
    'illustrations_illustrationoftheday_issues',
    'issues_issue',
    'notes_note',
    'notes_note_issues',
    'positions_issuecategoryposition',
    'positions_issuenoteposition',
    'quotas_categoryquota', 
    'regions_featuredregion',
    'regions_note',
    'regions_note_issues',
    'videos_video',
    'videos_video_issues',
    'voyages_article',
    'voyages_article_issues',
]

# Dump
# ------------------------------------------------------------------------------
for table in tables:
    command = 'mysqldump -u %s %s %s %s > dumps/%s' % (db_user, db_name, options, table, '%s.sql' % table)
    exec_command = os.system(command)
    print "Dump table %s... OK." % table

#command = 'mysqldump -u %s %s %s %s > %s' % (db_user, db_name, options, ' '.join(tables), 'dump.sql')
#exec_command = os.system(command)
#print "Dump tables... OK."
