# Scrapy settings for dongsport project
#__*__encoding:utf-8__*__
SPIDER_MODULES = ['quyundong.spiders']
NEWSPIDER_MODULE = 'quyundong.spiders'
COOKIES_ENABLES=True
ITEM_PIPELINES = {
    'quyundong.pipelines.JsonWriterPipeline': 800,
    'quyundong.pipelines.DBPipeline': 900,
}
#取消默认的useragent,使用新的useragent  
DOWNLOADER_MIDDLEWARES = {  
        'scrapy.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'rotate_useragent.RotateUserAgentMiddleware' :400
    }
LOG_LEVEL = 'INFO'
COOKIES_DEBUG = True