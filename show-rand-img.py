import os
from random import choice
import pygame
from time import sleep

#--- load image-files
start_path = input("path: ")
allfiles = os.walk(start_path)  #generator-object
fileslist = []
for path,dirs,files in allfiles:
    for filename in files:
        fileslist.append(os.path.join(path,filename))   # all image-paths in fileslist

        #--- setup pygame
pygame.init() 
screen_size_x = 1280
screen_size_y = 780 # Set the width and height of the screen
screen = pygame.display.set_mode((screen_size_x, screen_size_y))
pygame.display.set_caption("random image from" + start_path)
 
clock = pygame.time.Clock() # Used to manage how fast the screen updates

loop = True # Loop until the user clicks the close button.
while loop: # -------- Main Program Loop -----------
    # --- Main event loop
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # If user clicked close
            loop = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_SPACE:     # if spacebar
                screen.fill((0,0,0))    #(0,0,0)==black     #clear screen
                randomfile = choice(fileslist)  #load random filepath as string
                try: pic = pygame.image.load(randomfile).convert()       # load as image == pygame surface object
                except pygame.error:
                    print("couldnt load as image:", randomfile)
                    continue    
                #resize image to fit screen
                pic_size_x,pic_size_y = pic.get_size()
                ratio = pic_size_x/pic_size_y
                if pic_size_x > screen_size_x: 
                    pic = pygame.transform.scale(pic, (screen_size_x,int(screen_size_x/ratio)))
                if pic_size_y > screen_size_y: 
                    pic = pygame.transform.scale(pic, (int(screen_size_y*ratio), screen_size_y))
                screen.blit(pic, [0,0]) #image, position
                #print path
                font = pygame.font.SysFont('Arial', 14, True, False)
                text = font.render(randomfile, True, (0,0,0))
                screen.blit(text, [0, 0])
                
    pygame.display.flip()  # update screen
    clock.tick(60)      # --- Limit to frames per second
     
pygame.quit() # Close the window and quit.
