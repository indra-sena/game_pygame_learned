import pygame
import time
import random

pygame.init()

crash_sound = pygame.mixer.Sound("vehicle104.wav")

width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
bred = (255,0,0)
bgreen = (0,255,0)
bblue = (0,0,255)
block_color = (53,115,255)

car_width = 73
pause = False

display=pygame.display.set_mode((width,height))
pygame.display.set_caption('New Game')
clock = pygame.time.Clock()
#crashed = False

carimg = pygame.image.load('racecar.png')
gameIcon = pygame.image.load('Cars.png')
pygame.display.set_icon(gameIcon)


def things_dodged(count) :
    font = pygame.font.SysFont(None,25)
    text = font.render('Dodged: '+str(count),True,black)
    display.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color) :
    pygame.draw.rect(display, color, [ thingx, thingy, thingw, thingh ])

def car(x,y) :
    display.blit(carimg, (x,y))

def text_objects(text,font) :
    textSurface = font.render(text, True, black)
    return textSurface,textSurface.get_rect()

def message_display(text) :
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((width/2),(height/2))
    display.blit(TextSurf,TextRect)
    
    pygame.display.update()
    
    time.sleep(2)
    
    game_loop()

def crash() :
    
    #pygame.mixer.Sound.play(crash_sound)
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((width/2),(height/2))
    display.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button("Play Again",150,450,100,50,green,bgreen,game_loop)
        button("Quit",550,450,100,50,red,bred,quit)

        pygame.display.update()
        clock.tick(15) 

def button(msg,x,y,w,h,ic,ac,action = None) :
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y :
        pygame.draw.rect(display,ac,(x,y,w,h))
        
        if click[0] == 1 and action != None :
            action()
    else :
        pygame.draw.rect(display,ic,(x,y,w,h))
    smallText = pygame.font.Font('freesansbold.ttf',20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display.blit(textSurf, textRect)

def unpaused() :
    global pause
    pause = False

def paused() :
    
    while pause :
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
        button('Continue',150,450,100,50,green,bgreen,unpaused)
        button('Quit',550,450,100,50,red,bred,quit)
            
        pygame.display.update()
        clock.tick(15)

def game_intro() :
    
    intro = True
    while intro :
        for event in pygame.event.get() :
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Hello",largeText)
        TextRect.center = ((width/2),(height/2))
        display.blit(TextSurf,TextRect)
        
        button("Go!",150,450,100,50,green,bgreen,game_loop)
        button("Quit",550,450,100,50,red,bred,quit)
        
        pygame.display.update()
        clock.tick(15)
        
        
def game_loop() :
    x = width*0.45
    y = height*0.85
    
    x_change = 0
    #car_speed = 0
    thing_startx= random.randrange(0,width)
    thing_starty = -600
    thing_speed = 15
    thing_width = 100
    thing_height = 100
    
    thing_count = 1
    
    dodged = 0
    
    gameExit = False

    while not gameExit :
        global pause
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT :
                    x_change = -5
                elif event.key == pygame.K_RIGHT :
                    x_change = 5
                elif event.key == pygame.K_p :
                    pause = True
                    paused()
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    x_change = 0
            
        x += x_change
            
        display.fill(white)
        
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty +=thing_speed
        
        car(x,y)
        things_dodged(dodged)
            
        if x>width-car_width or x<0 :
            #x = width-car_width
            crash()
        #elif x<0 :
            #x = 0
        if thing_starty > height :
            thing_starty = 0-thing_height
            thing_startx = random.randrange(0,width)
            dodged +=1
            #thing_speed+=1
            #thing_width +=dodged*1.2
        if y < thing_starty +thing_height :
            print('y crossover')
            
            if x>thing_startx and x<thing_startx + thing_width or x+car_width>thing_startx and x+car_width<thing_startx+thing_width :
                print('x crossover')
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
