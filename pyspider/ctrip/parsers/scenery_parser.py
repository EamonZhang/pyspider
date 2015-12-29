#! /usr/bin/env python
# coding=utf-8


# from django.contrib.gis.geos.point import Point


class SceneryListParser(object):

    def __init__(self, scenery):
        self.scenery = scenery

    def get_parsed_info(self):
        scenery_info = {
            'address': self.scenery['Address'],
            'source_id': self.scenery['ID'],
            'img_base_url': '',
            'market_price': self.scenery['MarketPrice'],
            'name': self.scenery['Name'],
            'source_order_count': self.scenery['OrderCount'],
            'price': self.scenery['Price'],
            'source_price': self.scenery['Price'],
            'grade': int(self.scenery['Star']),
        }
        # 去除图片的尺寸信息
        if self.scenery['Image']:
            img_url = self.scenery['Image'].replace('_C_186_105', '')
            scenery_info['img_cover_path'] = img_url
            scenery_info['img_path_list'] = [img_url]
        return scenery_info


class SceneryDetailParser(object):

    def __init__(self, scenery):
        self.scenery = scenery

    def get_parsed_info(self):
        # 景区基本信息
        scenery_info = {
            'source_comment_count': self.scenery['CommentCount'],
            'score': self.scenery['CommentGrade'],
            'source_score': self.scenery['CommentGrade'],
            'available': self.scenery['IsCanBooking'],
#             'location': Point(self.scenery['Longitude'], self.scenery['Latitude']),
            'open_time': self.scenery['OpenTimeDesc'],
            'source_url': self.scenery['URL']
        }
        # 景区附加信息
        for scenery_detail in self.scenery['ProductList'][0]['ProductAddInfoList']:
            detail_name = scenery_detail['AddInfoSubTitleName']
            # 景区特色
            if detail_name == u'产品经理推荐':
                features = []
                for feature_info in scenery_detail['ProductAddInfoDetailList']:
                    features.append(feature_info['DescDetail'][1:])
                scenery_info['features'] = features
            # 景区交通信息
            if detail_name == u'交通信息':
                traffics = []
                for traffic_info in scenery_detail['ProductAddInfoDetailList']:
                    traffics.append(traffic_info['DescDetail'])
                scenery_info['traffic_info'] = '\n'.join(traffics)
        # 景区简介
        scenery_info['intro'] = self.scenery['ProductList'][0]['ProductDescriptionInfo']['Introduction']
        # 景区的门票信息
        ticket_list = self.scenery['ProductList']
        for ticket in ticket_list:
            ticket_info = {
                'ahead_time': ticket['AdvanceBookingTime'],  # TODO
                'ahead_day': ticket['AdvanceBookingDays'],
            }
            pass
        return scenery_info
