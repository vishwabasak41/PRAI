try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '966606789646082049-Jn11uTmH2eP8j0jHQ2lHokpIH4jYCQO'
ACCESS_SECRET = 'mgQrQHj4xuiRCuONRkaGCFQGNH5MAf56xnkuyzTLfAvPq'
CONSUMER_KEY = 'lJH9AoFxyxAnlDSSGuhnIqe2T'
CONSUMER_SECRET = 'SIKp6zVteGGGSplJLp02ntesza3TM4aa48DBPjhHsAqivrelBF'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count =100

for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    tweets= json.dumps(tweet).strip() 
    # print tweets
    # print "type os is",type(tweets)
    if 'text' in tweet : 
        if "lang"=="en":
            print "id=",tweet['id'] # This is the tweet's id
            print "Creted at:",tweet['created_at'] # when the tweet posted
            print "Content",tweet['text'] # content of the tweet
                        
            print tweet['user']['id'] # id of the user who posted the tweet
            print tweet['user']['name'] # name of the user, e.g. "Wei Xu"
            print tweet['user']['screen_name']
    # for line in tweets:
    #     try:
    #         print line
            # Read in one line of the file, convert it into a json object 
            # tweet = json.loads(line.strip())
            # print "tweet are------"
            # print tweet
        #     if 'text' in tweet: 
        #         print tweet['id'] # This is the tweet's id
        #         print tweet['created_at'] # when the tweet posted
        #         print tweet['text'] # content of the tweet
                            
        #         print tweet['user']['id'] # id of the user who posted the tweet
        #         print tweet['user']['name'] # name of the user, e.g. "Wei Xu"
        #         print tweet['user']['screen_name'] # name of the user account, e.g. "cocoweixu"

        #         hashtags = []
        #         for hashtag in tweet['entities']['hashtags']:
        #         	hashtags.append(hashtag['text'])
        #         print hashtags

        # except:
        #     # read in a line is not in JSON format (sometimes error occured)
        #     continue

    if tweet_count <= 0:
        break 
       
    
