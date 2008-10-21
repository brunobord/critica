# -*- coding: utf-8 -*-
"""
Critica utils for widgets.

"""
import re


def resize_widget(widget, width=300, height=241):
    """
    Resizes a widget.
    
    Required parameter::
    
        widget
            The (embedded) HTML widget.
            
    Optional parameters::
        
        width
            Widget width. By default: 300
            
        height
            Widget height. By default: 241
     
    """
    r_width = re.compile('(width="[0-9]+")')
    r_height = re.compile('(height="[0-9]+")')
    
    new_widget = re.sub(r_width, 'width="%d"' % width, widget)
    new_widget = re.sub(r_height, 'height="%d"' % height, new_widget)
    
    return new_widget


