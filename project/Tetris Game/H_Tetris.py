'''Importing Libraries'''
#Python libraries
import random, time, pygame, sys
#My libraries
import start_screen, main_menu
#Importing the necessary parts
from pygame.locals import *
#Importing from the other python files
from start_screen import *
from main_menu import *

#System setup
fps = 60           #Framerate of game
windowWidth = 800   #Width of game window
windowHeight = 700  #Height of game window
boxSize = 25        #Board scale
boardWidth = 10     #Board Width
boardHeight = 24    #Board Height
gameRunning = True

#Colours
#name         R   G   B
cyan =      ( 14,246,238) #I Piece
blue =      (  0,  2,230) #J Piece
orange =    (226,161, 35) #L Piece 
yellow =    (245,251, 24) #O Piece
green =     ( 42,233, 31) #S Piece
purple =    (226, 34,217) #T Piece
red =       (216, 11, 26) #Z Piece
white =     (255,255,255) #Text Colour
blueGrey =  ( 36, 63, 93) #Background Colour

while gameRunning:
    game_intro()
    main_menu()