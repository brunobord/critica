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
db_password = ''
options = '-e -t'
output_file = 'dump.sql'
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
    'positions_categoryposition',
    'positions_issuecategoryposition',
    'positions_issuenoteposition',
    'positions_noteposition',
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
command = 'mysqldump -u %s -p %s %s %s %s > %s' % (
    db_user, 
    db_password, 
    db_name, 
    options, 
    ' '.join(tables), 
    output_file)
    
exec_command = os.system(command)

print "Dumped tables in %s... OK." % output_file


