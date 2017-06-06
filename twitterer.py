#!/usr/bin/python3

from twython import Twython
import time

from pbconf import (
    t_consumer_key,
    t_consumer_secret,
    t_access_token,
    t_access_token_secret,
    archive_path,
    caption
    )
print("Contacting Twitter")

twitter=Twython(t_consumer_key,t_consumer_secret,t_access_token,t_access_token_secret)
now = time.strftime("%Y-%m-%d-%H-%M-%S")
print("Uploading to Twitter")
message = caption + now + " #TYO_Photo"
with open(archive_path + 'photobooth.jpg','rb') as photo:
    twitter.update_status_with_media(status=message, media=photo)
print("Tweeted")
