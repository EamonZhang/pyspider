#! /usr/bin/env python
# coding=utf-8


"""
从携程获取景区信息
"""


from gevent import monkey
monkey.patch_all(thread=False)
from django.core.management.base import BaseCommand

from ctrip.imports.scenery_info import SceneryApi


class Command(BaseCommand):

    def handle(self, *args, **options):
        SceneryApi.import_scenery_list()
        # SceneryApi.import_scenery_detail()
