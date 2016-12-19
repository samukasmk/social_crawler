# twitter-crawler
Crawler based on Twitter API with tapioca-wrapper and tapioca-twitter

type:
  instagram: 1
  twitter: 2

post_id
  instagram key: ["caption"]["id"]
  twitter   key: ["id"]

post_text
  instagram key: ["caption"]["text"]
  twitter   key: ["text"]

posted_at
  instagram key: ["caption"]["created_time"] - time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1353447503))
  twitter   key: ["created_at"]

user_name
  instagram key: ["caption"]["from"]["username"]
  twitter   key: ["user"]["screen_name"]

user_id
  instagram key: ["caption"]["from"]["id"]
  twitter   key: ["user"]["id"]

tags
  instagram key: ["tags"]                  - ', '.join()
  twitter   key: ["entities"]["hashtags"]  - ', '.join()

image
  instagram key: ["images"]["standard_resolution"]["url"]
  twitter   key: ["entities"]["media"][0]["media_url"]

total_likes
  instagram key: ["likes"]["count"]
  twitter   key: None
