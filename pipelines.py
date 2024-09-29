import mysql.connector

class MySQLPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hustler@8493',
            database='mynews'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS news_tb (
                id INT AUTO_INCREMENT PRIMARY KEY,
                headlines TEXT,
                latest_news TEXT,
                images LONGTEXT,
                UNIQUE KEY unique_headlines (headlines(512)),
                UNIQUE KEY unique_latest_news (latest_news(512)),
                UNIQUE KEY unique_images (images(512))
            )
        """)

    def process_item(self, items, spider):
        try:
            # Log item before storing in the database
            spider.logger.info(f"Processing items  in the pipeline: {items}")
            spider.logger.info(f"Images in the pipeline which are extracted: {items['images']}")
            if not items['images']:
             spider.logger.warning("No images found in the pipeline.")

            spider.logger.info(f"Full item received in the pipeline: {items}")
            
            # Store all items in the database
            self.store_all_items(items, spider)
            spider.logger.info(f"data   stored in the database: {items}")
        except Exception as e:
            spider.logger.error(f"Error storing item: {e}")
        return items

    def store_all_items(self, items, spider):
        # Extract individual items from lists
        headlines = items.get('headlines', [])
        latest_news = items.get('latest_news', [])
        images = items.get('images', [])
        spider.logger.info(f"Type of images: {type(images)}, Count: {len(images)}")
         #  Log the data you're extracting from items
        spider.logger.info(f"Extracted Headlines: {headlines}")
        spider.logger.info(f"Extracted News: {latest_news}")
        spider.logger.info(f"Extracted Images in the pipeline: {images}")
        spider.logger.info(f"Headline length: {len(items.get('headlines', ''))}")
        spider.logger.info(f"Image URL length: {len(items.get('images', ''))}")


        
        for headline, news, image in zip(headlines, latest_news, images):
            
            headline = headline.strip() if headline else 'No Headline'
            news = latest_news.strip() if news else 'No Latest News'
            image = image.strip() if image else 'No Image'

            # Log the data being inserted
            spider.logger.info(f"Inserting Headline: {headline}, Latest News: {news}, Image URL: {image}")
            


            # Check if the headline already exists
            self.curr.execute("""
                SELECT id FROM news_tb WHERE headlines = %s AND latest_news = %s AND images = %s

            """, (headline,news,image))
            result = self.curr.fetchone()
            spider.logger.info(f"{result}")

            if result is None:
                try:
                    # Insert data
                    self.curr.execute("""
                        INSERT INTO news_tb (headlines, latest_news, images)
                        VALUES (%s, %s, %s)
                    """, (headline, news, image))
                    spider.logger.info("inserting data successfully")
                    self.conn.commit()
                except Exception as e:
                    spider.logger.error(f"Error executing SQL query: {e}")
                    self.conn.rollback()  
            else:
                spider.logger.info(f"Skipping duplicate headline: {headline}")
