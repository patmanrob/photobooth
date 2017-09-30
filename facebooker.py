#!/usr/bin/python

import facebook
import time

from pbconf import(
    fb_page_id,
    fb_access_token,
    caption,
    archive_path
    )

print("Contacting Facebook")

graph=facebook.GraphAPI(fb_access_token)
#resp = graph.get_object('me/accounts')
#page_access_token = None
#for page in resp['data']:
#    if page['id']== fb_page_id:
#        page_access_token=page['access_token']
#    graph=facebook.GraphAPI(page_access_token)
    

print("Uploading")

now = time.strftime("%H:%M")
status= graph.put_photo(image=open(archive_path +'photobooth.jpg','rb'), message = caption + now + " #TYO_Photo")
print("Uploaded to Facebook")




