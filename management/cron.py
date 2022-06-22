# from django.core.management import call_command
import tweepy
import requests
from management.models import TwitterAd, FacebookAd

"""

Twitter and Facebook AD management Scripts below

"""


def advertisement():
    """
    This function will post the latest Facebook Ad
    """
    twitter_context = TwitterAd.objects.all().first()
    facebook_context = FacebookAd.objects.all().first()
    apiKey = twitter_context.twitter_api_key
    apiSecret = twitter_context.twitter_api_secret
    accessToken = twitter_context.twitter_access_token
    accessTokenSecret = twitter_context.twitter_access_token_secret

    # 3. Create Oauth client and set authentication and create API object
    oauth = tweepy.OAuthHandler(apiKey, apiSecret)
    oauth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(oauth)

    # 4. upload media
    # media = api.media_upload("code.png")

    api.update_status(
        status=twitter_context.tweet_description,
    )

    """
        This function will post the latest Facebook Ad
    """

    facebook_page_id = facebook_context.facebook_page_id
    access_token = facebook_context.facebook_access_token
    url = "https://graph.facebook.com/{}/photos".format(facebook_page_id)
    msg = facebook_context.post_description
    image_location = "https://images.unsplash.com/photo-1655495171748-0062a08dd98d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1529&q=80"
    payload = {
        "url": image_location,
        "access_token": access_token,
        "message": msg,
    }

    # Send the POST request
    requests.post(url, data=payload)
