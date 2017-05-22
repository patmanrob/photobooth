#!/usr/bin/python

import time, os, subprocess
from gpiozero import Button
import picamera
import facebook
from pbconf import(
	file_path,
	fb_upload,
	tw_upload,
	em_upload
	)




button=Button(21)
camera=picamera.PiCamera()
camera.vflip=False
camera.hflip=False

def main():
	while True:
		print ("Ready")
		button.wait_for_press()#wait for button press to start
		snap=0
		camera.start_preview()
		time.sleep(2)
		while snap<4:
			print ("Taking Pic") #take 4 photos
			now = time.strftime("%Y-%m-%d-%H-%M-%S")
			#camera.start_preview()
			time.sleep(2) #warm up camera
			filename = file_path + now + '.jpg'
			camera.capture(filename)
			print(filename)
			#camera.stop_preview()
			snap+=1
		camera.stop_preview()
		print("Montaging")#Make the montage
		subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
		if fb_upload==True:
			if os.path.isfile('/home/pi/scripts/photobooth/facebooker.py')==True:
				print("Facebooker is there,")
				subprocess.call("/home/pi/scripts/photobooth/facebooker.py")
				print ("Facebooker Done")
		if tw_upload==True:
			if os.path.isfile('/home/pi/scripts/photobooth/twitterer.py')==True:
				print("Twitterer is there, uploading to Twitter")
				subprocess.call("/home/pi/scripts/photobooth/twitterer.py")
				print("Twitterer done")
		if em_upload==True:
			if os.path.isfile('/home/pi/scripts/photobooth/mailer.py')==True:
				print("Emailer is there. Sending")
				subprocess.call("/home/pi/scripts/photobooth/mailer.py")
				print("Emailrer done")
		print("ready for next round")
   



if __name__ == "__main__":
  main()
