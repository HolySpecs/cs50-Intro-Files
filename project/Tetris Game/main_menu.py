#Importing Python modules
import pygame,time
#Importing Game modules
import start_screen, infinite, sprint
from start_screen import *
from infinite import *
from sprint import *
from leaderboard import *

#Starting the Pygame module
pygame.init()

#Variables
controller = False
displayWidth = 800
displayHeight = 700
display = pygame.display.set_mode((displayWidth, displayHeight))

#Allowing the String to be displayed on the screen
def text_format(message, textFont, textSize, textColour):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColour)
    return newText

#Colours used
#              R    G    B
white =     (255, 255, 255)
black =     (  0,   0,   0)
grey =      ( 50,  50,  50)
red =       (255,   0,   0)
green =     (  0, 255,   0)
blue =      (  0,   0, 255)
yellow =    (255, 255,   0)
blueGrey =  ( 36,  63,  93)

#Font to be used
font = 'Calibri.ttf'

#Frames per second allowed
clock = pygame.time.Clock()
FPS = 60

#The Main Menu Function
def main_menu():
    #Sound Effects
    menuMusic = 'audio files/Music/Menu Music.ogg'
    menuNav = 'audio files/Sound Effects/Menu Nav.ogg'
    menuSelect = 'audio files/Sound Effects/Menu Select.ogg'
    menu = True
    #Default option
    selected = 1
    #Start Music Service
    pygame.mixer.init()
    #BGM Channel
    channel1 = pygame.mixer.Channel(0)
    #Sound Effects Channel
    channel2 = pygame.mixer.Channel(1)
    channel1.play(pygame.mixer.Sound(menuMusic),-1)
    #Configuring Controller
    controller = False
    try:
        j = pygame.joystick.Joystick(0)
        j.init()
        controller = True
    except:
        pass
    while menu == True:
        for event in pygame.event.get():
            #When the Cross button on the window is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            '''Menu Nav for Keyboard'''
            if event.type == pygame.KEYDOWN:
                channel2.play(pygame.mixer.Sound(menuNav))
                #Menu navigation
                if event.key == pygame.K_UP: #Move up
                    selected = selected - 1
                elif event.key == pygame.K_DOWN: #Move Down
                    selected = selected + 1
                if event.key == pygame.K_RETURN: #Confirm is pressed
                    channel2.play(pygame.mixer.Sound(menuSelect))
                    #If the option selected is infinte
                    if selected == 1:
                        #Test confirm
                        print('infinite')
                        time.sleep(1)
                        pygame.display.update()
                        #returns back to the first option
                        selected = 1
                        pygame.mixer.quit()
                        #Plays the game
                        infinite(win)
                        #starts the music for the main menu
                        pygame.mixer.init()
                        channel1.play(pygame.mixer.Sound(menuMusic),-1)
                    elif selected == 2:
                        #Not implemented yet
                        print('Sprint')
                        time.sleep(1)
                        pygame.display.update()
                        selected = 2
                        pygame.mixer.quit()
                        sprint(win)
                        pygame.mixer.init()
                        channel1.play(pygame.mixer.Sound(menuMusic), -1)
                    elif selected == 3:
                        #Not implemented yet
                        print('Leaderboard')
                        time.sleep(1)
                        pygame.display.update()
                        selected = 3
                        leaderboard(win)
                    elif selected == 4:
                        time.sleep(1)
                        pygame.quit()
                        quit()
                if event.key == pygame.K_RSHIFT:
                    channel2.play(pygame.mixer.Sound(menuSelect))
                    time.sleep(1)
                    #exits menu loop and therefore returns back to start screen
                    menu = False
            '''Menu Nav for Controller'''
            #DPad Controls
            if controller == True:
                dPad = j.get_hat(0)
                if dPad == (0,1):
                    #Pressing the Up button
                    channel2.play(pygame.mixer.Sound(menuNav))
                    selected = selected - 1
                elif dPad == (0,-1):
                    #Pressing the Down button
                    channel2.play(pygame.mixer.Sound(menuNav))
                    selected = selected + 1
            #Button Controls
                if event.type == pygame.JOYBUTTONDOWN:
                    if j.get_button(2):
                        #Pressing the Confirm button
                        channel2.play(pygame.mixer.Sound(menuSelect))
                        #The same as the ones for the keyboard
                        # If the option selected is infinte
                        if selected == 1:
                            # Test confirm
                            print('infinite')
                            time.sleep(1)
                            pygame.display.update()
                            # returns back to the first option
                            selected = 1
                            pygame.mixer.quit()
                            # Plays the game
                            infinite(win)
                            # starts the music for the main menu
                            pygame.mixer.init()
                            channel1.play(pygame.mixer.Sound(menuMusic), -1)
                        elif selected == 2:
                            # Not implemented yet
                            print('Sprint')
                            time.sleep(1)
                            pygame.display.update()
                            selected = 2
                            pygame.mixer.quit()
                            sprint(win)
                            pygame.mixer.init()
                            channel1.play(pygame.mixer.Sound(menuMusic), -1)
                        elif selected == 3:
                            # Not implemented yet
                            print('Leaderboard')
                            time.sleep(1)
                            pygame.display.update()
                            selected = 3
                            leaderboard(win)
                        elif selected == 4:
                            time.sleep(1)
                            pygame.quit()
                            quit()
                    elif j.get_button(1):
                        #Pressing the Circle Button
                        channel2.play(pygame.mixer.Sound(menuSelect))
                        time.sleep(1)
                        #exits menu loop and therefore returns back to start screen
                        menu = False
            #Loop back if bottom/top is reached
            if selected > 4:
                selected = 1
            elif selected < 1:
                selected = 4
        #The looks of the text
        display.fill(blueGrey)
        title = text_format('Main Menu', font, 64, white)
        buttonC = text_format('X or Enter - Confirm', font, 40, white)
        buttonB = text_format('O or Right Shift - Back', font, 40, white)
        if selected == 1: #Highlighted
            textInfinite = text_format('Infinite', font, 50, white)
        else: #Not Highlighted
            textInfinite = text_format('Infinite', font, 50, grey)
        if selected == 2:
            textSprint = text_format('Sprint', font, 50, white)
        else:
            textSprint = text_format('Sprint', font, 50, grey)
        if selected == 3:
            textLeaderBoard = text_format('Leaderboard', font, 50, white)
        else:
            textLeaderBoard  = text_format('Leaderboard', font, 50, grey)
        if selected == 4:
            textQuit = text_format('Quit', font, 50, white)
        else:
            textQuit = text_format('Quit', font, 50, grey)
        #Get the Dimensions of the text
        titleRect = title.get_rect()
        buttonCRect = buttonC.get_rect()
        buttonBRect = buttonB.get_rect()
        infiniteRect = textInfinite.get_rect()
        sprintRect = textSprint.get_rect()
        leaderBoardRect = textLeaderBoard.get_rect()
        quitRect = textQuit.get_rect()

        #Position of text
        base_x = displayWidth/3.5 -(titleRect[2]/1.5)
        display.blit(title, (base_x, 40))

        display.blit(textInfinite, (base_x, 150))
        display.blit(textSprint, (base_x, 212))
        display.blit(textLeaderBoard, (base_x, 275))
        display.blit(textQuit, (base_x, 337))
        display.blit(buttonC, (displayWidth/1.05 - (buttonCRect[2]), 600))
        display.blit(buttonB, (displayWidth/1.05 - (buttonBRect[2]), 640))
        #Refreshing the window to show updates
        pygame.display.update()
        clock.tick(FPS)
        #Window name
        pygame.display.set_caption('Tetris Hard Mode')
