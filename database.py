# import sqlite3

# # Connect to SQLite database
# conn = sqlite3.connect('news.db')
# curr = conn.cursor()

# # Create the table if it doesn't exist
# curr.execute("""
#     CREATE TABLE IF NOT EXISTS news_tb (
#         headlines TEXT unique,
#         latest_news TEXT unique,
#         images TEXT  unique,
#         news_title TEXT unique,
#         k_headlines TEXT unique
#     )
# """)
