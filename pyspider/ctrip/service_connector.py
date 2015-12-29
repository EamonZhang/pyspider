#! /usr/bin/env python
# coding=utf-8


import hashlib
import json
import time

import requests

from ctrip.config import CTRIP_SOURCE
from json.decoder import JSONDecoder


class CtripService(object):

    @classmethod
    def get_response(cls, interface, request_type, request_body):
        timestamp_str = str(int(time.time()))
        request_params = {
            'AllianceID': CTRIP_SOURCE['ALLIANCE_ID'],
            'SID': CTRIP_SOURCE['SID'],
            'ProtocolType': 1,
            'Signature': cls._calc_signature(timestamp_str, request_type),
            'TimeStamp': timestamp_str,
            'Channel': 'Vacations',
            'Interface': interface,
            'IsError': False,
            'RequestBody': json.dumps(request_body, ensure_ascii=False),
            'ResponseBody': '',
            'ErrorMessage': '',
        }
        payload = {
            'RequestJson': json.dumps(request_params, ensure_ascii=False).encode('GB2312')
        }
        print CTRIP_SOURCE['SERVICE_URL']
        print payload
        result = json.loads(requests.post(
            CTRIP_SOURCE['SERVICE_URL'],
            payload).content)
        if result['ErrorMessage']:
            raise Exception()  # TODO
        return json.loads(result['ResponseBody'])

    @classmethod
    def _calc_signature(cls, timestamp, request_type):
        client_md5 = hashlib.md5(CTRIP_SOURCE['SECRET_KEY']).hexdigest().upper()
        param = '%s%s%s%s%s' % (timestamp, CTRIP_SOURCE['ALLIANCE_ID'], client_md5, CTRIP_SOURCE['SID'], request_type)
        return hashlib.md5(param).hexdigest().upper()
