from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.conf import settings

from authlib.integrations.django_client import OAuth
from oauthlib.oauth2 import WebApplicationClient
#from authlib.oauth2.auth import 
from .models import TumblrAccount
# Create your views here.
from requests import utils
from urllib.parse import urlencode

def index(request : HttpRequest):
    logged_in_as = request.session.get("tumblraccount.name",  None)
    if logged_in_as is None:
        return render(request, "tumblrlogin/login.html")

def cb():
    pass

oauth = OAuth()
tumblr_oauth = oauth.register("tumblr")


tumblr = WebApplicationClient(
    client_id=settings.OAUTH_CONSUMER_KEY,
    response_type="code",
    scope=" ".join([]),
    # state is automatically hjandled
    state="meow",
    redirect_uri=settings.OAUTH_REDIRECT_URL,
)
def login(request):
    # https://www.tumblr.com/docs/en/api/v2#oauth2authorize---authorization-request
    print(tumblr_oauth)
    print(type(tumblr_oauth))
    #request()
    return redirect(
        tumblr.prepare_request_uri("https://www.tumblr.com/oauth2/authorize")
    )
    #return redirect(f"https://www.tumblr.com/oauth2/authorize?client_id=prtjh0DtZ4pbrLtSHQlI3BnZxsTynDobxyORyTxy6CCDRwBLns&response=code&redirect_uri=http://localhost:8000&state=meow")
    #return tumblr_oauth.authorize_redirect(request)
