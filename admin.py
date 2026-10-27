# pylint: disable=line-too-long
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django

from django.contrib.gis import admin

if django.get_version() < '5':
    from django.contrib.gis.admin import OSMGeoAdmin as GISModelAdmin # pylint: disable=no-name-in-module
else:
    from django.contrib.gis.admin import GISModelAdmin # pylint: disable=no-name-in-module

from .models import ExternalDataSource, ExternalDataRequest, ExternalDataRequestFile # pylint: disable=wrong-import-position

@admin.register(ExternalDataSource)
class ExternalDataSourceAdmin(GISModelAdmin):
    list_display = ('name', 'identifier', 'priority',)
    list_filter = ('name', 'identifier',)

@admin.register(ExternalDataRequest)
class ExternalDataRequestAdmin(GISModelAdmin):
    list_display = ('pk', 'requested', 'identifier', 'email', 'can_email', 'last_emailed', 'completed',)
    list_filter = ('requested', 'sources', 'can_email',)
    search_fields = ('identifier', 'token', 'extras',)

@admin.register(ExternalDataRequestFile)
class ExternalDataRequestFileAdmin(GISModelAdmin):
    list_display = ('request', 'id', 'source', 'uploaded', 'processed', 'skipped', 'encrypted',)
    list_filter = ('processed', 'skipped', 'uploaded', 'source', 'request')
