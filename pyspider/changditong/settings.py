# Scrapy settings for dongsport project
#__*__encoding:utf-8__*__
SPIDER_MODULES = ['changditong.spiders']
NEWSPIDER_MODULE = 'changditong.spiders'
COOKIES_ENABLES=False
ITEM_PIPELINES = {
    'changditong.pipelines.JsonWriterPipeline': 100,
    'changditong.pipelines.DBPipeline': 500,
    #图片下载管道
#     'scrapy.contrib.pipeline.images.ImagesPipeline': 300,
}
#取消默认的useragent,使用新的useragent  
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'rotate_useragent.RotateUserAgentMiddleware' :400
    }

#图片存储路径
IMAGES_STORE = '/home/zhangjin/data/changditong'
# 90天的图片失效期限
IMAGES_EXPIRES = 90
#日志级别
LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 60*20
