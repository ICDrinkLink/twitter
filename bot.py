from secret import access_token, access_token_secret, consumer_key, consumer_secret
import tweepy
import random

def setTwitterAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def tweetHelloWorld(api):
    api.update_status("This is an automated tweet using a bot! Hello, World!")

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        un = status.author.screen_name
        print(un)
        print(status.text)
        api.update_status("@" + un + "  This is a automated reply #{}".format(random.randint(0, 10000)), status.id)

if __name__ == "__main__":
    api = setTwitterAuth()
    # tweetHelloWorld(api)
    # user = api.me()
    # print(user.screen_name)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['DrinkLinkBot'], async=True)

