
import tweepy
import json

class scraper():

    def __init__(self):
        
        consumer_key = "CNnLUVKtLvvktAQd0fIuV0Rnj"
        consumer_secret = "Adze0YOeSHTcOIr8gdc4idpMTuZz52x0a12hgWEXbFjM9oGY5Y"
        access_token = "1302926283010052097-v2Z7WOumXj97QgvHdyMRyvEGUEeUX0"
        access_token_secret = "yaUL8SWyifip3lWunIHhYiwVXWIB2VEdze7P9kzyPDB9B"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        pass

    def __WriteJson(self, json_data): #write data.json
        with open("data.json", mode="a") as f:
            f.write(json.dumps(json_data) + '\n') #add \n at the end of line
        print(json_data)

    def __Get_PlaceID(self): #Country Level
        return self.api.geo_search(query='USA', granularity='country')[0].id

    def __Get_Posts(self, nums, place_id): #searching certain tweets
        return tweepy.Cursor(self.api.search, q='place:{}'.format(place_id)+ ' -filter:retweets',lang="en", locale='en', count=30000, tweet_mode='extended').items(nums)

    def Start_Search(self, nums): #num of tweets to search
        
        place_id = self.__Get_PlaceID()
        Posts = self.__Get_Posts(nums, place_id)

        for post in Posts:
            #print (post.full_text + " | " + post.place.name if post.place else "Undefined place")
            #if(post.place.name) 
            self.__WriteJson(post._json)

s = scraper()

s.Start_Search(30000)
