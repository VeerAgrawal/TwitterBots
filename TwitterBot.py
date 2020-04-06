import tweepy
import logging
import config
import time
import os

logger = logging.getLogger()
#add the keys repectivly
def create_api():
    consumer_key = " "
    consumer_secret = " "
    access_token = " "
    access_token_secret = " "

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

api = create_api()

botMessage = '''
There are 3 bots avaliable.
1) Find out the mutual followers of 2 acounts. 
2) Automaticly reply to people using specific keywords in their tweets.
3) automaticly follow all of your followers 
'''
print (botMessage)
bot = input ("which Bot would you like to use(1, 2, or 3): ")

def bot1():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    userName1 = input("what is the twitter username of one acount: ") 
    userName2 = input("what is the twitter username of anouther acount: ") 

    logger.info("Gathering followers of both acounts")

    firstAcountFollowers = api.followers(userName1)
    firstAcountFollowers2 = []

    for n in firstAcountFollowers:
        firstAcountFollowers2.append(n._json['screen_name'])

    secondAcountFollowers = api.followers(userName2)
    secondAcountFollowers2 = []

    for n in secondAcountFollowers:
        secondAcountFollowers2.append(n._json['screen_name'])

    mutalFollowers = []
    logger.info("searching for mutual followers")

    for x in firstAcountFollowers2:
        for y in secondAcountFollowers2:
            if x == y:
                mutalFollowers.append(x)

    listLenght = len(mutalFollowers)

    if listLenght > 0:
        print (f'{userName1} and {userName2} have {listLenght} mutual followers that are: {mutalFollowers}')
    elif listLenght == 0:
        print (f'{userName1} and {userName2} have 0 mutual followers')


def bot2():

    Key1 = input("Type a keyword you want to search for: ")
    Key2 = input("Typer anouther keyword you want to search for: ")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    def check_mentions(api, keywords, since_id):
        logger.info("Retrieving mentions")
        new_since_id = since_id
        for tweet in tweepy.Cursor(api.mentions_timeline,
            since_id=since_id).items():
            new_since_id = max(tweet.id, new_since_id)
            if tweet.in_reply_to_status_id is not None:
                continue
            if any(keyword in tweet.text.lower() for keyword in keywords):
                logger.info(f"Answering to {tweet.user.name}")

                if not tweet.user.following:
                    tweet.user.follow()

                api.update_status(
                    status="Please reach us via DM",
                    in_reply_to_status_id=tweet.id,
                )
        return new_since_id

    def main():
        api = create_api()
        since_id = 1
        while True:
            since_id = check_mentions(api, [Key1, Key2], since_id)
            logger.info("Waiting to find mentions of keywords")
            time.sleep(60)

    if __name__ == "__main__":
        main()

def bot3():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    def follow_followers(api):
        logger.info("Retrieving and following followers")
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                logger.info(f"Following {follower.name}")
                follower.follow()

    def main():
        api = create_api()
        while True:
            follow_followers(api)
            logger.info("You currently follow all your followers. Waiting for more...")
            time.sleep(60)

    if __name__ == "__main__":
        main()

if bot == '1':
    print ('''
    Bot1:
    This bot will identify the mutual followers of 2 accounts. 
    ''')
    bot1()
elif bot == '2':
    print(''' 
    Bot2:
    This bot will search for tweets in which you are mentioned 
    and check for specific keywords of your choice. The bot will 
    also make sure that it is not a reply to anouther tweet. If all 
    these requirments are met, then the bot will reply to the person. 

    Press 'Control C' to end the Program
    ''')
    bot2()
elif bot == '3':
    print('''
    Bot3:
    This bot will follow all of your followers that you are not currently following.
    The bot will search for new followers every 60 seconds. 

    Press 'Control C' to end the Program
    ''')
    bot3()
else:
    print ('Invalid Response: Please choose a number from 1 to 3. Restart the Program')
