#!/usr/bin/python

import sys
import time, os, subprocess
from gpiozero import Button
import picamera
import facebook
import pygame
from pbconf import(
	image_path,
	fb_upload,
	tw_upload,
	em_upload,
	image_path,
	archive_path,
    media_path,
    background,
    overlay,
    caption
	)




button=Button(21)
camera=picamera.PiCamera()
camera.vflip=False
camera.hflip=True
camera.rotation= 90

size = width, height = 1280, 720
black = 0,0,0
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Photo booth')
pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()

def clear_screen():
    screen.fill((0,0,0))
    pygame.display.flip()

def show_pic():
    screen.fill((0,0,0))
    img=pygame.image.load(archive_path+"photobooth.jpg")
    img=img.convert()
    img=pygame.transform.scale(img,(size))
    screen.blit(img,(1,1))
    pygame.display.flip()

def show_image(image):
    screen.fill((0,0,0))
    path=media_path+image
    print(path)
    img=pygame.image.load(path)
    img=img.convert()
    img=pygame.transform.scale(img,(size))
    screen.blit(img,(1,1))
    pygame.display.flip()
    


def main():
    try:
        while True:
            print ("Ready")
            show_image("ptb.png")
            button.wait_for_press()#wait for button press to start
            print("Button Pressed")
            show_image("sap.png")
            time.sleep(2)
            show_image("3.png")
            time.sleep(0.5)
            show_image("2.png")
            time.sleep(0.5)
            show_image("1.png")
            time.sleep(0.5)
            clear_screen()
            snap=1
            camera.start_preview()
            time.sleep(2)
            while snap<=4:
                print ("Taking Pic "+ str(snap)) #take 4 photos
                now = time.strftime("%Y-%m-%d-%H-%M-%S")
                time.sleep(2) #warm up camera
                filename = image_path + now + '.jpg'
                camera.hflip=False
                camera.capture(filename, resize=(968,648))
                camera.hflip=True
                print(filename)
                snap+=1
            camera.stop_preview()
            print("Montaging")#Make the montage
            show_image("proc.png")
            montager()
            if fb_upload==True:
                if os.path.isfile('/home/pi/photobooth/facebooker.py')==True:
                    print("Facebooker is there,")
                    show_image("ufb.png")
                    subprocess.call("/home/pi/photobooth/facebooker.py")
                    print ("Facebooker Done")
            if tw_upload==True:
                if os.path.isfile('/home/pi/photobooth/twitterer.py')==True:
                    print("Twitterer is there, uploading to Twitter")
                    show_image("utt.png")
                    subprocess.call("/home/pi/photobooth/twitterer.py")
                    print("Twitterer done")
            if em_upload==True:
                if os.path.isfile('/home/pi/photobooth/mailer.py')==True:
                    print("Emailer is there. Sending")
                    subprocess.call("/home/pi/photobooth/mailer.py")
                    print("Emailrer done")
            show_image("ad.png")
            time.sleep(2)
            print("ready for next round")
    except KeyboardInterrupt:
		keepgoing=False
		pygame.quit()
		sys.exit()
		return 0


def montager():
    print("Montaging inside python")
    montage_command="montage "+image_path+"*.jpg -tile 2x2 -geometry +30+30 -texture "+media_path+background+" "+image_path+"temp_montage2.jpg"
    print("Trying montage with variable   "+montage_command)
    subprocess.call(montage_command, shell=True)
    print("Done Montaging, adding overlay")
    show_image("at.png")
    montage_command2="composite -gravity center "+media_path+overlay+" "+image_path+"temp_montage2.jpg "+image_path+"temp_montage3.jpg"
    subprocess.call(montage_command2, shell=True)
    print("Done, saving montage")
    save_command="cp "+image_path+"temp_montage3.jpg "+archive_path+"$(date +%F_%T).jpg"
    subprocess.call(save_command, shell=True)
    save_command2="cp "+image_path+"temp_montage3.jpg "+archive_path+"photobooth.jpg"
    subprocess.call(save_command2, shell=True)
    print("Done, cleaning up")
    clean_up="rm "+image_path+"*.jpg"
    subprocess.call(clean_up, shell=True)
    show_pic()
    time.sleep(5)

if __name__ == "__main__":
  main()
