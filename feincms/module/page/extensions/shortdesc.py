#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adds a shortdesc field to the page
"""

import logging

from django.utils.translation import ugettext_lazy as _
from django.db import models
from feincms.module.page.models import Page
from mediamanager.models import Picture
from feincms._internal import monkeypatch_method


@monkeypatch_method(Page)
def rootline(self):
    rl = [self]
    p = self.parent
    while p:
        rl.insert(0, p)
        p = p.parent
    return rl

def register(cls, admin_cls):
    PIC_POS = ((u'l', _(u'left')),
                 (u'r', _(u'right')),
                 (u't', _(u'top')),
                 (u'b', _(u'bottom')),
               )

    cls.add_to_class('sd_head',
                     models.CharField(max_length=127, verbose_name=_('headline')))

    cls.add_to_class('sd_desc',
                     models.TextField(max_length=255,
                                      verbose_name=_('description text')))

    cls.add_to_class('sd_pic',
                     models.ForeignKey(Picture, blank=True, null=True,
                              verbose_name=_('picture')))

    cls.add_to_class('sd_pic_pos',
                     models.CharField(max_length=1, choices=PIC_POS, default=u'l',
                                      verbose_name=_('picture position')))


    if admin_cls and admin_cls.fieldsets:
        fieldsets = [ f for f in admin_cls.fieldsets ]
        
        admin_cls.raw_id_fields = list(admin_cls.raw_id_fields) + ['sd_pic']
        
        if fieldsets:
            shortdesc_fields = (_('short description'),
                                {'fields':['sd_head', 'sd_desc', 'sd_pic', 'sd_pic_pos']})
            fieldsets = [fieldsets[0], shortdesc_fields] + fieldsets[1:]
            admin_cls.fieldsets = fieldsets
        else:
            logging.warning("Couldn't determine which fieldset on %s should have the shortdesc fields", admin_cls)
