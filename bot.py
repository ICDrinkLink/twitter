from secret import access_token, access_token_secret, consumer_key, consumer_secret
import tweepy
import random
from emoji import UNICODE_EMOJI
import requests
import os

MAX_ALCOHOLS = 4
MAX_MIXERS = 2

emojiMap = {
    "😅😂🤣😢😭😰😥😓😪" : "Vodka",
    "🙃😕🙁☹😟" : "Cider",
    "😋😛😝😜🤪🤑" : "Beer 🍻",
    "😀😃😄😁😆😫😩" : "Rum",
    "😯😦😧😮😲😵" : "Whisky 🥃",
    "😡🤬😱😨🤯😳😚🤗" : "Tequila",
    "🤔🤭🤫🤢🤮" : "Jagermeister",
    "🧐🤓😎🤨🤩😍😉" : "Bailey",
    "😇😈👿🤕🤤" : "Wine 🍷",
    "☺😏😒😞😔😤" : "Gin",
}

drinkingGames = {
    "Around the World 🌎" : "https://en.wikipedia.org/wiki/Around_the_World_(card_game)",
    "Avalanche ❄️" : "https://en.wikipedia.org/wiki/Avalanche_(drinking_game)",
    "Bartok (card game)" : "https://en.wikipedia.org/wiki/Bartok_(card_game)",
    "Baseball ⚾" : "https://en.wikipedia.org/wiki/Baseball_(drinking_game)",
    "Beer checkers" : "https://en.wikipedia.org/wiki/Beer_checkers",
    "Beer die 🎲" : "https://en.wikipedia.org/wiki/Beer_die",
    "Beer mile" : "https://en.wikipedia.org/wiki/Beer_mile",
    "Beer pong 🏓" : "https://en.wikipedia.org/wiki/Beer_pong",
    "Boat Race 🚣‍♂️" : "https://en.wikipedia.org/wiki/Boat_race_(game)",
    "Buffalo 🐃" : "https://en.wikipedia.org/wiki/Buffalo_(game)",
    "Caps" : "https://en.wikipedia.org/wiki/Caps_(drinking_game)",
    "Detonator 💣" : "https://en.wikipedia.org/wiki/Detonator_(game)",
    "Dizzy Bat 🦇" : "https://en.wikipedia.org/wiki/Dizzy_bat",
    "Edward Fortyhands ✂️" : "https://en.wikipedia.org/wiki/Edward_Fortyhands",
    "Flip Cup" : "https://en.wikipedia.org/wiki/Flip_cup",
    "Fuzzy Duck 🦆" : "https://en.wikipedia.org/wiki/Fuzzy_Duck_(drinking_game)",
    "Goon of Fortune" : "https://en.wikipedia.org/wiki/Goon_of_Fortune",
    "Horserace 🐴" : "https://en.wikipedia.org/wiki/Horserace_(drinking_game)",
    "Kinito" : "https://en.wikipedia.org/wiki/Kinito",
    "Never Have I Ever" : "https://en.wikipedia.org/wiki/Never_Have_I_Ever",
    "Pyramid" : "https://en.wikipedia.org/wiki/Pyramid_(drinking_game)",
    "Ring of Fire 🔥" : "https://en.wikipedia.org/wiki/Kings_(game)",
    "Ride the Bus 🚌" : "https://en.wikipedia.org/wiki/Ride_the_bus"
}

listOfGames = ["Around the World 🌎", "Avalanche ❄️", "Bartok (card game)", "Baseball ⚾", "Beer checkers", "Beer die 🎲",
               "Beer mile", "Beer pong 🏓", "Boat Race 🚣‍♂️", "Buffalo 🐃", "Caps", "Detonator 💣", "Dizzy Bat 🦇", "Edward Fortyhands ✂️",
               "Flip Cup", "Fuzzy Duck 🦆", "Goon of Fortune", "Horserace 🐴", "Kinito", "Never Have I Ever", "Pyramid",
               "Ring of Fire 🔥", "Ride the Bus 🚌"]
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

class EmojiDrinkListener(tweepy.StreamListener):

    def on_status(self, status):
        tweetText = status.text

        if ("#cocktail" in tweetText.lower()):
            self.randomCocktail(status)
        elif ("#games" in tweetText.lower()):
            self.games(status)
        else:
            self.emojiDrink(status)

    def games(self, status):
        userScrName = status.author.screen_name

        gameName = listOfGames[random.randint(0, len(listOfGames) - 1)]
        link = drinkingGames[gameName]

        api.update_status("@" + userScrName + " Game: " + gameName + "\n\nMore Info: " + link, status.id)

    def emojiDrink(self, status):
        userScrName = status.author.screen_name
        tweetText = status.text
        tweetText = tweetText.replace("@DrinkLinkBot", "")
        tweetText = tweetText.replace(" ", "")
        tweetText = tweetText.replace("\n", "")

        alcoCount = 0
        mixCount = 0

        message = ""

        print(tweetText)
        print(len(tweetText))

        for emoji in tweetText:
            if (len(message) < 140) and (emoji != "\n"):
                alcoholFunc = getAlcohol(emoji, alcoCount, mixCount)
                alcoCount = alcoholFunc[1]
                mixCount = alcoholFunc[2]
                if (alcoholFunc[0] != "") and (alcoholFunc[0] not in message):
                    message += alcoholFunc[0] + ", "

        message = message[:-2]

        if message != "":
            api.update_status("@" + userScrName + " Here's Your Drink 🍸: " + message, status.id)
        else:
            api.update_status("@" + userScrName + " Please tweet me emojis to get your mix or #Cocktail for a random cocktails", status.id)

    def randomCocktail(self, status):
        userScrName = status.author.screen_name

        url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"
        response = requests.request("GET", url)
        json = response.json()["drinks"][0]

        ingredients = []

        nameStub = "strIngredient"
        amountStub = "strMeasure"

        for i in range(1, 16):
            if json[nameStub + str(i)] != "":
                ingredients.append(json[amountStub + str(i)] + json[nameStub + str(i)])

        message1 = "Your Cocktail 🍹 is " + "'" + json["strDrink"] + "'" + " served in a " + json["strGlass"] + ". " + "Ingredients: " + ", ".join(ingredients)
        instruction = "Instructions: " + json["strInstructions"]

        filename = 'temp.jpg'
        url = json["strDrinkThumb"]

        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            api.update_status("@" + userScrName + " " + instruction, status.id)
            api.update_with_media(filename, "@" + userScrName + " " + message1, in_reply_to_status_id = status.id)

            os.remove(filename)

if __name__ == "__main__":
    api = setTwitterAuth()

    emojiDrinkListener = EmojiDrinkListener()
    emojiDrink = tweepy.Stream(auth=api.auth, listener=emojiDrinkListener)
    emojiDrink.filter(track=['@DrinkLinkBot'], async=True)