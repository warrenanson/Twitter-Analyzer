
import tweepy
import json

class scraper():

    def __init__(self):
        
        consumer_key = "ssaVncgqH8vq1tsljpBouGUCT"
        consumer_secret = "mQh1h6yjNqecIYxYdv4HYXwvnZv4YIlyPArDcAW2Q9rGa2OvNG"
        access_token = "749926510610436096-cQnAkoND5Z3CM5ibT3gEhTp9Ha9Z347"
        access_token_secret = "Tzwk8oJae8fg5TezDq2vjOr2RcJ1c1N0K8HP3DVFiIO2I"

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
