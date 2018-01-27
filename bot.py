from secret import access_token, access_token_secret, consumer_key, consumer_secret
import emojiMapping
import tweepy
import random
from emoji import UNICODE_EMOJI

MAX_ALCOHOLS = 4
MAX_MIXERS = 2

emojiMap = {
    "😅😂🤣😢😭😰😥😓😪" : "Vodka",
    "🙃😕🙁☹😟" : "Cider",
    "😋😛😝😜🤪🤑" : "Beer",
    "😀😃😄😁😆😫😩" : "Rum",
    "😯😦😧😮😲😵" : "Whisky",
    "😡🤬😱😨🤯😳😚🤗" : "Tequila",
    "🤔🤭🤫🤢🤮" : "Jagermeister",
    "🧐🤓😎🤨🤩😍😉" : "Bailey",
    "😇😈👿🤕🤤" : "Wine",
    "☺😏😒😞😔😤" : "Gin",
}

listOfMixers = ["Coke", "Lemonade", "Cranberry Juice", "Orange Juice", "Apple Juice", "Tonic Water", "Cream Soda", "Sparkling Water"]

def getAlcohol(emoji, alcoCount, mixCount):
    for key in emojiMap.keys():
        if (emoji in key) and (alcoCount < MAX_ALCOHOLS):
            return [emojiMap[key], alcoCount + 1, mixCount]

    if (emoji in UNICODE_EMOJI) and (mixCount < MAX_MIXERS):
        return [listOfMixers[random.randint(0, len(listOfMixers) - 1)], alcoCount, mixCount + 1]

    return ["", alcoCount, mixCount]


def setTwitterAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        userScrName = status.author.screen_name
        tweetText = status.text
        tweetText = tweetText.replace("@DrinkLinkBot", "")
        tweetText = tweetText.replace("#Mix", "")
        tweetText = tweetText.replace(" ", "")
        tweetText = tweetText.replace("\n", "")

        alcoCount = 0
        mixCount = 0

        message = ""

        print(tweetText)
        print(len(tweetText))

        for emoji in tweetText:
            if (len(message) < 120) and (emoji != "\n"):
                alcoholFunc = getAlcohol(emoji, alcoCount, mixCount)
                alcoCount = alcoholFunc[1]
                mixCount = alcoholFunc[2]
                if (alcoholFunc[0] != "") and (alcoholFunc[0] not in message):
                    message += alcoholFunc[0] + ", "

        message = message[:-2]

        api.update_status("@" + userScrName + " Here's Your Drink: " + message, status.id)


if __name__ == "__main__":
    api = setTwitterAuth()
    # tweetHelloWorld(api)
    # user = api.me()
    # print(user.screen_name)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['DrinkLinkBot'], async=True)

    # tweetText = "@DrinkLinkBot 😂🤨⛄ #DrinkLinkMix"
    # tweetText = tweetText.replace("@DrinkLinkBot", "")
    # tweetText = tweetText.replace("#DrinkLinkMix", "")
    # tweetText = tweetText.replace(" ", "")
    #
    # message = ""
    #
    # for emoji in tweetText:
    #     if len(message) < 120:
    #         message += emojiMapping.getAlcohol(emoji) + ", "
    #
    # print(message)