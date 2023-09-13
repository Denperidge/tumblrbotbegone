from secrets import token_urlsafe

from django.shortcuts import render, redirect, HttpResponse
from django.http.request import HttpRequest
from django.conf import settings

from authlib.integrations.django_client import OAuth
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.tokens import OAuth2Token
#from authlib.oauth2.auth import 
from .models import TumblrAccount
# Create your views here.
from requests import post
from urllib.parse import urlencode
from urllib.request import urlopen, Request

from pytumblr import TumblrRestClient, TumblrRequest

from requests import get

from tumblrbotbegone.utils import tumblr_client


def index(request : HttpRequest):
    print(type(request.session.get("access_token")))
    
    access_token = request.session.get("access_token",  None)
    print(access_token)

    if access_token:


        client = tumblr_client(access_token["access_token"])
        return HttpResponse(str(client.info()))
    
    return render(request, "tumblrlogin/login.html")


def logout(request):
    request.session.clear()
    return redirect("index")
    


oauth = OAuth()
tumblr_oauth = oauth.register("tumblr")


tumblr = WebApplicationClient(
    client_id=settings.OAUTH_CONSUMER_KEY,
    
    response_type="code",
    scope=" ".join(["basic", "offline_access"]),
    # state is automatically hjandled
    redirect_uri=settings.OAUTH_REDIRECT_URL,
)
def login(request: HttpRequest):
    # https://www.tumblr.com/docs/en/api/v2#oauth2authorize---authorization-request
    request.session["state"] = token_urlsafe()
    request.session.save()
    #request()
    return redirect(
        tumblr.prepare_request_uri("https://www.tumblr.com/oauth2/authorize", state=request.session.get("state"))
    )
    #return redirect(f"https://www.tumblr.com/oauth2/authorize?client_id=prtjh0DtZ4pbrLtSHQlI3BnZxsTynDobxyORyTxy6CCDRwBLns&response=code&redirect_uri=http://localhost:8000&state=meow")
    #return tumblr_oauth.authorize_redirect(request)

def redirect_callback(request: HttpRequest):
    if not request.GET.get("state") or request.GET.get("state") != request.session.get("state"):
        return HttpResponse("State missing")
    else:
        token_req = tumblr.prepare_token_request(
            "https://api.tumblr.com/v2/oauth2/token", 
            request.build_absolute_uri().replace("http://", "https://"), 
            state=request.session.get("state"), 
            client_secret=settings.OAUTH_CONSUMER_SECRET)
        # Thanks to https://stackoverflow.com/a/36485152

        access_token = post(url=token_req[0], data=token_req[2], headers=token_req[1]).json()

        request.session["access_token"] = access_token
        request.session.save()

        return redirect("index")