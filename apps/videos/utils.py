# -*- coding: utf-8 -*-
"""
Utils of ``critica.apps.videos`` application.

"""
import re


VIDEO_DEFAULT_WIDTH = 300
VIDEO_DEFAULT_HEIGHT = 241


def resize_video(widget):
    """
    Resizes video widget.
    
    Required parameter::
    
        widget
            The (embedded) HTML widget.
     
    """
    r_width = re.compile('(width="[0-9]+")')
    r_height = re.compile('(height="[0-9]+")')
    
    new_widget = re.sub(r_width, 'width="%d"' % VIDEO_DEFAULT_WIDTH, widget)
    new_widget = re.sub(r_height, 'height="%d"' % VIDEO_DEFAULT_HEIGHT, new_widget)
    
    return new_widget


