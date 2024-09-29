import os
import requests
import scrapy
from ..items import NewsscrapingItem

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    page_number = 2
    start_urls = [
        'https://greaterkashmir.com',
        'https://www.greaterkashmir.com/kashmir',
        'https://www.greaterkashmir.com/business'
    ]

    def parse(self, response):
        self.logger.info(f"Scraping from the greater kashmir: {response.url}")
        

        items = NewsscrapingItem()

        # Extract data
        headlines = response.css('h2 a::text').extract()
        latest_news = response.css('.entry-title a::text').extract()
        images = response.css('img.wp-post-image::attr(src)').extract()

        self.logger.info(f"Extracted headlines: {headlines}")
        self.logger.info(f"Extracted latest news: {latest_news}")
        self.logger.info(f"Extracted images in the spider: {images}")

        # Save images and their paths
        image_paths = []
        for i, img_url in enumerate(images):
            # Download the image and save it to a local folder
            img_name = f'image_{i}.jpg'
            img_path = os.path.join('downloaded_images', img_name) 
            self.download_image(img_url, img_path)
            image_paths.append(img_path)

        items['headlines'] = headlines
        items['latest_news'] = latest_news
        items['images'] = images  
    
        self.logger.info(f"Item to be yielded to the pipeline: {items}")
        yield items

        # Handle pagination
        next_page = response.css('a.page-numbers::attr(href)').get()
        if next_page:
            self.logger.info(f"Following pagination to: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("No more pages to scrape.")

        # Handle pagination for 'Business' section
        if "business" in response.url:
            next_page = f'https://www.greaterkashmir.com/business/page/{self.page_number}/'
            if self.page_number < 2:
                self.page_number += 1
                yield response.follow(next_page, callback=self.parse)

    def download_image(self, img_url, img_path):
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(response.content)
            self.logger.info(f"Image saved to: {img_path}")
