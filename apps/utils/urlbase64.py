# -*- coding: utf-8 -*-
"""
Utils to encode and decode URLs.

Borrowed from: http://www.djangosnippets.org/snippets/1004/

"""
import base64


def uri_b64encode(s):
    """
    Encodes URI.
    
    """
    return base64.urlsafe_b64encode(s).strip('=')


def uri_b64decode(s):
    """
    Decodes URI.
    
    """
    return base64.urlsafe_b64decode(s + '=' * (len(s) % 4))

