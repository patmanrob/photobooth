#!/usr/bin/python3

from twython import Twython
import time

from pbconf import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    archive_path
    )
print("Contacting Twitter")

twitter=Twython(consumer_key,consumer_secret,access_token,access_token_secret)
now = time.strftime("%Y-%m-%d-%H-%M-%S")
print("Uploading to Twitter")
message = "Hello from Pi3 at " + now
with open(archive_path + 'photobooth.jpg','rb') as photo:
    twitter.update_status_with_media(status=message, media=photo)
print("Tweeted")
