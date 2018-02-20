import os
from random import choice
import pygame
from time import sleep

class Pic():
    """class to hold the image"""
    def __init__(self):
        self.surface = None
        self.path=""
        self.xdim, self.ydim = 0,0
        self.ratio = 0
        self.xdim_original = 0
        self.ydim_original = 0
        
    def fit_to_screen(self, screen_size_x, screen_size_y):
        if self.xdim > screen_size_x: self.surface = pygame.transform.scale(self.surface, (screen_size_x,int(screen_size_x/self.ratio)))
        if self.ydim > screen_size_y: self.surface = pygame.transform.scale(self.surface, (int(screen_size_y*self.ratio), screen_size_y))
        self.xdim_original=self.xdim
        self.ydim_original=self.ydim
        self.xdim, self.ydim = self.surface.get_size()
        
def new_random_pic(fileslist):
    while True:
        randomfilepath = choice(fileslist)  #load random filepath as string
        try:
            surf = pygame.image.load(randomfilepath).convert()       # load as image == pygame surface object
            break
        except pygame.error: print("couldnt load as image:", randomfilepath)
    pic = Pic()
    pic.path=randomfilepath
    pic.surface=surf
    pic.xdim, pic.ydim = pic.surface.get_size()
    pic.ratio = pic.xdim/pic.ydim
                    
    return pic
    
def main():
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
    pygame.display.set_caption("random image from " + start_path)
     
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
                    pic = new_random_pic(fileslist)
                    pic.fit_to_screen(screen_size_x,screen_size_y)
                    #resize image to fit screen                  
                    screen.blit(pic.surface, [0,0]) #image, position
                    pygame.display.set_caption(pic.path)
                    
        pygame.display.flip()  # update screen
        clock.tick(60)      # --- Limit to frames per second
         
    pygame.quit() # Close the window and quit.

if __name__=="__main__":
    main()

