#!/usr/bin/python

import time, os, subprocess
from gpiozero import Button
import picamera
import facebook
from pbconf import(
	image_path,
	fb_upload,
	tw_upload,
	em_upload
	)




button=Button(21)
camera=picamera.PiCamera()
camera.vflip=False
camera.hflip=False
camera.rotation= 90


def main():
	while True:
		print ("Ready")
		button.wait_for_press()#wait for button press to start
		print("Button Pressed")
		snap=1
		camera.start_preview()
		time.sleep(2)
		while snap<=4:
			print ("Taking Pic "+ str(snap)) #take 4 photos
			now = time.strftime("%Y-%m-%d-%H-%M-%S")
			time.sleep(2) #warm up camera
			filename = image_path + now + '.jpg'
			camera.capture(filename, resize=(968,648))
			print(filename)
			snap+=1
		camera.stop_preview()
		print("Montaging")#Make the montage
		montager()
		if fb_upload==True:
			if os.path.isfile('/home/pi/photobooth/facebooker.py')==True:
				print("Facebooker is there,")
				subprocess.call("/home/pi/photobooth/facebooker.py")
				print ("Facebooker Done")
		if tw_upload==True:
			if os.path.isfile('/home/pi/photobooth/twitterer.py')==True:
				print("Twitterer is there, uploading to Twitter")
				subprocess.call("/home/pi/photobooth/twitterer.py")
				print("Twitterer done")
		if em_upload==True:
			if os.path.isfile('/home/pi/photobooth/mailer.py')==True:
				print("Emailer is there. Sending")
				subprocess.call("/home/pi/photobooth/mailer.py")
				print("Emailrer done")
		print("ready for next round")
   

def montager():
	print("Montaging inside python")
	subprocess.call("montage /home/pi/photobooth/images/*.jpg -tile 2x2 -geometry +30+30 -texture /home/pi/photobooth/media/background.jpg /home/pi/photobooth/images/temp_montage2.jpg", shell=True)
	print("Done Montaging, adding overlay")
	subprocess.call("composite -gravity center /home/pi/photobooth/media/overlay.png /home/pi/photobooth/images/temp_montage2.jpg /home/pi/photobooth/images/temp_montage3.jpg", shell=True)
	print("Done, saving montage")
	subprocess.call("cp /home/pi/photobooth/images/temp_montage3.jpg /home/pi/photobooth/archive/$(date +%F_%T).jpg", shell=True)
	subprocess.call("cp /home/pi/photobooth/images/temp_montage3.jpg /home/pi/photobooth/archive/photobooth.jpg", shell=True)
	print("Done, cleaning up")
	subprocess.call("rm /home/pi/photobooth/images/*.jpg", shell=True)

if __name__ == "__main__":
  main()
