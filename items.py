import scrapy

class NewsscrapingItem(scrapy.Item):
    headlines = scrapy.Field()
    latest_news = scrapy.Field()
    images = scrapy.Field()

    # KASHMIRNEWS
   
