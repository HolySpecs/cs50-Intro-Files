'''Importing Libraries'''
import pygame,time, sys
from pygame.locals import *

pygame.init()

'''Variables'''
#Checking if a controller is connected or not
controller = False
try:
    #Initiates and checks if a controller is connected
    j = pygame.joystick.Joystick(0)
    j.init()
    #Allows Controls for the controller to be used
    controller = True
except:
    pass
#How fast the game will run
FPSCLOCK = pygame.time.Clock()
#Size of display
displayWidth = 800
displayHeight = 700
#Colours needed
#             R   G   B
white =    (255,255,255)   # Font Colour
blueGrey = ( 36, 63, 93)   # Background colour
#Loading images
tetrisImg = pygame.image.load('images/tetris-logo.png')        # The Tetris logo
titleBar = pygame.image.load('images/bar 360 by 100.png')      # The Title bar

#function for if the cross button on the window is clicked
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

#Returning text to draw
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

#Closing the game and the python screen
def terminate():
    pygame.quit()
    sys.exit()

#Window heading
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Teris Hard Mode')
clock = pygame.time.Clock()

'''The start screen'''
def game_intro():
    pygame.mixer.quit() #Ending previous Audio in prevous tracks
    pygame.mixer.init() #Starting Music Service
    pygame.mixer.music.load('audio files/Music/tetris theme remix.ogg') #Start Theme
    pygame.mixer.music.play(-1, 0.0) #Play Infinitely
    intro = True
    while intro == True:
        #The background Screen        
        gameDisplay.fill(blueGrey)
        #The Font and their Sizes
        mediumText = pygame.font.Font('freesansbold.ttf',30)
        #Variables for Drawing Images and text
        TextSurf1, TextRect1 = text_objects("Press Enter or Start to Begin", mediumText)
        '''Drawing the Text and Images on the screen'''
        #Images
        gameDisplay.blit(tetrisImg, ((displayWidth/4),(displayHeight/64)))
        #Text
        TextRect1.center = ((displayWidth/2),(displayHeight/1.5))
        gameDisplay.blit(TextSurf1, TextRect1)
        #Updating the screen
        pygame.display.update()
        clock.tick(60)
        '''Exiting the start screen'''
        for event in pygame.event.get():
            #Checking if the window needs to be closed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #Exiting the Start screen
            if event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #Loading and playing the menu select effect
                    pygame.mixer.init()
                    pygame.mixer.music.load('audio files/Sound Effects/Menu Select.ogg')
                    pygame.mixer.music.play(1)
                    intro = False
            if controller == True:
                if event.type == pygame.JOYBUTTONDOWN:
                    if j.get_button(9):
                        pygame.mixer.init() #Starting the music service
                        #Playing the specific file
                        pygame.mixer.music.load('audio files/Sound Effects/Menu Select.ogg')
                        #Letting it be played once
                        pygame.mixer.music.play(1)
                        #Exiting the start screen loop
                        intro = False