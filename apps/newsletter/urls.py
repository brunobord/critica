# -*- coding: utf-8 -*-
"""
URLs of ``critica.apps.newsletter`` application.

newsletter_subscribe_form
-------------------------

Displays newsletter subscribing form.

- Named URL   : ``newsletter_subscribe_form``
- View        : ``critica.apps.newsletter.views.subscribe_form``
- Arguments   : None

newsletter_subscribe_thanks
---------------------------

Displays newsletter subscribing thanks message.

- Named URL   : ``newsletter_subscribe_thanks``
- View        : ``critica.apps.newsletter.views.subscribe_thanks``
- Arguments   : None

newsletter_unsubscribe_form
---------------------------

Displays newsletter unsubscribing form.

- Named URL   : ``newsletter_unsubscribe_form``
- View        : ``critica.apps.newsletter.views.unsubscribe_form``
- Arguments   : None

newsletter_unsubscribe_thanks
-----------------------------

Displays newsletter unsubscribing thanks message.

- Named URL   : ``newsletter_unsubscribe_thanks``
- View        : ``critica.apps.newsletter.views.unsubscribe_thanks``
- Arguments   : None

"""
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url('^desabonner/a-bientot/$',
        'critica.apps.newsletter.views.unsubscribe_thanks',
        name='newsletter_unsubscribe_thanks',
    ),
    url('^desabonner/$',
        'critica.apps.newsletter.views.unsubscribe_form',
        name='newsletter_unsubscribe_form',
    ),
    url('^merci/$', 
        'critica.apps.newsletter.views.subscribe_thanks', 
        name='newsletter_subscribe_thanks',
    ),
    url('^$', 
        'critica.apps.newsletter.views.subscribe_form', 
        name='newsletter_subscribe_form',
    ),
)

