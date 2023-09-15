from django.conf import settings

from pytumblr import TumblrRestClient, TumblrRequest

def tumblr_client(oauth_token: str=None, token_type="Bearer"):
    client = TumblrRestClient(
        consumer_key=settings.OAUTH_CONSUMER_KEY,
        consumer_secret=settings.OAUTH_CONSUMER_SECRET)
    request = TumblrRequest(
        consumer_key=settings.OAUTH_CONSUMER_KEY,
        consumer_secret=settings.OAUTH_CONSUMER_SECRET
    )

    if oauth_token:
        request.oauth = None
        request.headers["Authorization"] = f"{token_type} {oauth_token}"

    client.request = request
    
    return client