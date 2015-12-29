#! /usr/bin/env python
# coding=utf-8


from collections import Counter
import logging
import time

import gevent.pool

from ctrip.config import POOL_NUM
from ctrip.parsers.scenery_parser import SceneryDetailParser
from ctrip.parsers.scenery_parser import SceneryListParser
from ctrip.service_connector import CtripService
# from sceneries.config import ctrip_theme_dict
# from sceneries.models import CtripSceneryModel


logger = logging.getLogger('import_ctrip_scenery_info')


class SceneryApi(object):

    @staticmethod
    def _get_theme_list():
        request_body = {
            'DistributionChannel': 9,
            'PagingParameter': {
                'PageIndex': 1,
                'PageSize': 100
            },
            'SearchParameter': {
                # 'Keyword': '',
                # 'SaleCityID': 1
            }
        }
        result = CtripService.get_response('TicketSenicSpotSearch', 'TicketSenicSpotSearch', request_body)
        for label_info in result['LabelSatistics']:
            if label_info['LableType'] == 'MD_ScenicSpotFilterLabelGroup_Themes':
                themes = label_info['SubLabelSatistics']
                ctrip_theme_list = []
                for theme in themes:
                    ctrip_theme_list.append(theme['LabelText'])
                return ctrip_theme_list

    @staticmethod
    def import_scenery_list():
        counter = Counter()
        start_time = time.time()

        def import_scenery_list_task(theme_name):
            page_num = 0
            while True:
                page_num += 1
                request_body = {
                    'DistributionChannel': 9,
                    'PagingParameter': {
                        'PageIndex': page_num,
                        'PageSize': 100
                    },
                    'SearchParameter': {
                        'Keyword': theme_name,
                        # 'SaleCityID': 1
                    }
                }
                result = CtripService.get_response('TicketSenicSpotSearch', 'TicketSenicSpotSearch', request_body)
                scenery_list = result['ScenicSpotListItemList']
                if not scenery_list:
                    break
                for scenery in scenery_list:
                    parser = SceneryListParser(scenery)
                    parsed_scenery = parser.get_parsed_info()
                    # 补充主题信息
                    parsed_scenery['source_theme_name'] = theme_name
#                     if theme_name in ctrip_theme_dict:
#                         theme_id = ctrip_theme_dict[theme_name]['id']
#                     else:
#                         theme_id = ctrip_theme_dict[u'其他']['id']
                    # 入库
                    source_id = parsed_scenery['source_id']
#                     CtripSceneryModel.add_or_update(source_id, parsed_scenery)
#                     CtripSceneryModel.update_theme_ids(source_id, theme_id)
                    counter['scenery'] += 1
            logger.info('获取主题为%s的携程景区列表完成，共%s个景区' % (theme_name, counter['scenery']))

        logger.info('开始获取携程景区列表')
        pool = gevent.pool.Pool(POOL_NUM)
        ctrip_theme_list = SceneryApi._get_theme_list()
        pool.map(import_scenery_list_task, ctrip_theme_list)
        logger.info('获取携程景区列表已完成，用时%.2f秒' % (time.time() - start_time))

    @staticmethod
    def import_scenery_detail():

        def import_scenery_detail_task(id_list):
            request_body = {
                'DistributionChannel': 9,
                'ResponseDataType': 0,
                'ID': id_list,
                'ProductId': None,
                'DebugKey': None,
                'ImageSize': None,
            }
            result = CtripService.get_response('TicketSenicSpotInfo', 'TicketSenicSpotInfo', request_body)
            scenery_list = result['ScenicSpotList']
            for scenery in scenery_list:
                parser = SceneryDetailParser(scenery)
                scenery_info = parser.get_parsed_info()

#         pool = gevent.pool.Pool(POOL_NUM)
#         all_source_ids = CtripSceneryModel.get_source_ids()
#         source_id_list = []
#         for index in range(0, len(all_source_ids))[::20]:
#             # 一次查询20个景区
#             source_id_list.append(all_source_ids[index:index+20])
#         pool.map(import_scenery_detail_task, source_id_list)
if __name__ == '__main__':
    ls = SceneryApi._get_theme_list()
    for l in ls:
        print l 