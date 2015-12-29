# Scrapy settings for dongsport project
#__*__encoding:utf-8__*__
SPIDER_MODULES = ['dongsport.spiders']
NEWSPIDER_MODULE = 'dongsport.spiders'
COOKIES_ENABLES=False
ITEM_PIPELINES = {
   'dongsport.pipelines.JsonWriterPipeline': 800,
   'dongsport.pipelines.DBPipeline': 900,
}
#取消默认的useragent,使用新的useragent  
DOWNLOADER_MIDDLEWARES = {  
        'scrapy.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'rotate_useragent.RotateUserAgentMiddleware' :400
    }
IMAGE_BASE_PASH = "/home/zhangjin/data/dongsportimage/"
LOG_LEVEL = 'INFO'
#-----------------------------------数据库配置---------------------------------------
DB_DATA = "crawldata"
DB_USER_NAME="postgres"
DB_PWD="123456"
DB_HOST="192.168.6.28"
DB_PORT="5432"
CREATE_TABLE_SQL = """ 
        CREATE TABLE dongsport_base_create_talbe_data
        (
          sport_id character varying,
          name character varying,
          tag character varying,
          address character varying,
          lon character varying,
          lat character varying
        )
        WITH (
          OIDS=FALSE
        );
        ALTER TABLE dongsport_base_create_talbe_data
          OWNER TO postgres;
          
        CREATE TABLE dongsport_deepinfo_create_talbe_data
        (
          sport_id character varying,
          facilities character varying,
          traffic character varying,
          book character varying,
          intruduction character varying,
          images character varying
        )
        WITH (
          OIDS=FALSE
        );
        ALTER TABLE dongsport_deepinfo_create_talbe_data
          OWNER TO postgres;
       """