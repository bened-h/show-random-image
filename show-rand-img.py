import os
from random import choice
import pygame
from time import sleep


class Pic():
    """class to hold the image"""
    shown_pics = []
    def __init__(self):
        self.surface = None
        self.path=""
        self.xdim, self.ydim = 0,0
        self.ratio = 0
        self.xdim_original = 0
        self.ydim_original = 0
        self.shown_pics.append(self)
        
    def fit_to_screen(self, screen_size, fill_screen = False):
        screen_size_x, screen_size_y = screen_size
        if self.xdim > screen_size_x: self.surface = pygame.transform.scale(self.surface, (screen_size_x,int(screen_size_x/self.ratio)))
        elif fill_screen: self.surface = pygame.transform.scale(self.surface, (screen_size_x,int(screen_size_x/self.ratio)))
        if self.surface.get_size()[1] > screen_size_y: self.surface = pygame.transform.scale(self.surface, (int(screen_size_y*self.ratio), screen_size_y))
        self.xdim_original, self.ydim_original=self.xdim, self.ydim
        self.xdim, self.ydim = self.surface.get_size()
        
def get_new_random_pic(fileslist, fill_screen = False):
    
    #get pic
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
    screen_size_x = 1800
    screen_size_y = 980
    randunten = 20
    screen_size = screen_size_x , screen_size_y # Set the width and height of the screen
    screen_size_pic = screen_size_x , screen_size_y -randunten
    screen = pygame.display.set_mode(screen_size)
    font = pygame.font.SysFont('Calibri', 12, True, False)
    pygame.display.set_caption("random image from " + start_path)
    index = 0   # number of pic shown 
     
    clock = pygame.time.Clock() # Used to manage how fast the screen updates
    fill_screen = True

    loop = True # Loop until the user clicks the close button.
    while loop: # -------- Main Program Loop -----------
        # --- Main event loop
        for event in pygame.event.get():    # User did something
            if event.type == pygame.QUIT:   # If user clicked close
                loop = False
            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_SPACE:     # if spacebar
                    pic = get_new_random_pic(fileslist)
                    pic.fit_to_screen(screen_size_pic, fill_screen) #resize image to fit screen                  
                    #show pic
                    screen.fill((0,0,0))    #(0,0,0)==black     #clear screen
                    screen.blit(pic.surface, [screen_size_x/2-pic.xdim/2,0]) #image, position
                    pygame.display.set_caption(pic.path) #update caption
                    index = len(Pic.shown_pics)
                elif event.key == pygame.K_d:  # delete image
                    os.remove(pic.path)
                    screen.fill((0,0,0))    #(0,0,0)==black     #clear screen
                    Pic.shown_pics.remove(pic)
                    print(pic.path + " deleted.")
                    text = font.render(pic.path+ " deleted.", True, (255,255,255))
                    screen.blit(text, [0, 0])
                elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                    loop = False
                elif event.key == pygame.K_LEFT:
                    if index!=0: index-=1
                    else: continue
                    pic = Pic.shown_pics[index]
                    screen.fill((0,0,0))    #(0,0,0)==black     #clear screen
                    screen.blit(pic.surface, [screen_size_x/2-pic.xdim/2,0]) #image, position
                    pygame.display.set_caption(pic.path) #update caption#todo: show prev. pic
                    
        pygame.display.flip()  # update screen
        clock.tick(30)      # --- Limit to frames per second
         
    pygame.quit() # Close the window and quit.

if __name__=="__main__":
    main()

