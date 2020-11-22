import tweepy
import csv
import helpers

api = None
def SetupApi(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

helpers.loadDictionaries()

"""
Get user information
"""
def GetUserTweets(username, items=50):
    user_tweets = []
    try:
        for status in tweepy.Cursor(api.user_timeline, id=username).items(items):
            user_tweets.append(status.text)
    except:
        return None
    else:
        return user_tweets

def GetUserTopCategories(tweets):
    categories = {}
    for tweet in tweets:
        cat, score = helpers.getCategory(tweet)
        #print(cat, "-", score)
        #print(tweet,"\n", "cat: ", cat)
        if cat in categories:
            categories[cat] += score
        else:
            categories[cat] = score

    sorted_cat = sorted(categories.items(), key=lambda v : v[1], reverse=True)
    return sorted_cat

"""
Compare user categories
"""
def CheckSimilarCatergories(cat_user1, cat_user2, top=3):
    # [(cat, score), (cat, score)...(cat, score)]
    print("User1:",cat_user1, "\nUser2:",cat_user2)
    similar_cats = []
    for i in range(min(len(cat_user1), top)):
        for j in range(min(len(cat_user2), top)):
            if cat_user1[i][0] == cat_user2[j][0]:
                #print(cat_user1[i][1], cat_user2[j][1])
                similar_cats.append(cat_user1[i][0])
            
    return similar_cats

#tweets_teorema_galleta = ["Mama knows best", "cleaning is fun when no one ask you to do it","I want to go fashion drive to go to ride my girl","ready for tomorrow!", "ready for today!", "ready to plug in my baby","Camouflage paint stands upon somebody else's legs.","Stew and rum wants to set things right.","A river a thousand paces wide brings both pleasure and pain.","Abstraction would die for a grapefruit!","A classical composition stole the goods.","A passionate evening says goodbye to the shooter.","Two-finger John approaches at high velocity!","Chair number eleven is f***ing cosmopolitan, having a trained assassin stay overnight, letting heartbreaking lies roll over us like a summer breeze.","Nihilism would kindly inquire something about you.","That way doesn't like paying taxes.","An old apple likes to take a walk in the park."]
#tweets_teorema_cantu = ["Item drop 1 is go for launch! Unlock the new MTN DEW emblem and Doritos charm in @CallofDuty #BlackOpsColdWar right now. Make sure you follow us, then tweet @MountainDew with #DoritosDewDrop to get your code.","Republican Senator Pat Toomey said it was time for Donald Trump to concede that Joe Biden won the presidential election","The craziest part about Justin Herbert being the frontrunner for Rookie of the Year is that he's only 14 years old.","The prehistoric flying reptile with oddly dark bones belongs to a genus named after House Targaryen in Game of Thrones","Anxiety over how to keep a president’s power in check dates as far back as the 1787 Constitutional Convention","Plants may have unexpected resources that could help them survive—and perhaps even thrive—in a hotter, more carbon-rich future","Arrested at 17 for capital murder, I shot no one, triggerman was identified, I was at the scene but didn't have a gun, still in prison 18 yrs later, bail was denied. 17 yr old Kyle shot 3 people. All I can say is him & his family have been treated a lot better than me and mine.", "In case you didn’t think our Solar System was amazing, try Europa, a moon of Jupiter that seems to glow in the dark!","Science is what we understand well enough to explain to a computer. Art is everything else we do. -Donald Knuth"]

def GetSimilarity(user1, user2):
    tweets_user1 = GetUserTweets(user1)
    tweets_user2 = GetUserTweets(user2)
    if not tweets_user1:
        return "User {} not found".format(user1)
    if not tweets_user2:
        return "User {} not found".format(user2)
    cats_user1 = GetUserTopCategories(tweets_user1) 
    cats_user2 = GetUserTopCategories(tweets_user2)
    return CheckSimilarCatergories(cats_user1, cats_user2)