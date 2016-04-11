from httplib import HTTPConnection
from urlparse import urlparse
import requests
key="7233245e498f12569d29dc8910ee5cb2"
def get_twishort_uri(url):
 try:
  return url.split("twishort.com/")[1]
 except IndexError:
  return False

def get_full_text(uri):
 r = requests.get("http://api.twishort.com/1.1/get.json", params={"uri": uri, "api_key": key})
 return r.json()["text"]