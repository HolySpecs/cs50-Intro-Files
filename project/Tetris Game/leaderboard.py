import pygame, sys
from csv import reader

pygame.init()

white = (255, 255, 255)
displayWidth = 800
displayHeight = 700

#Allowing the String to be displayed on the screen
def text_format(message, textFont, textSize, textColour):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColour)
    return newText

def import_data(file_name):
    with open(file_name, 'r') as file:
        database = list(reader(file))
    return database

def time_converter(milliseconds):
    seconds = round(int(milliseconds) / 1000, 2)
    minutes = round(seconds // 60)
    seconds = round(seconds - (minutes * 60),2)
    if seconds < 10:
        return "{0}:0{1}".format(minutes, seconds)
    else:
        return "{0}:{1}".format(minutes, seconds)

#music needs to be added
def leaderboard(window):
    #import data
    #separtate the data
    #place into a table
    #format the data on the screen
    clock = pygame.time.Clock()
    scores = import_data('infinite.csv')
    times = import_data('sprint.csv')
    #add headers to the tables
    scores.insert(0,["Name", "Score"])
    times.insert(0, ["Name", "Time"])
    menuNav = 'audio files/Sound Effects/Menu Nav.ogg'
    menuSelect = 'audio files/Sound Effects/Menu Select.ogg'
    channel2 = pygame.mixer.Channel(1)
    #format the times in the times database
    for i in range(1, len(times)):
        times[i][1] = time_converter(times[i][1])
    #choice 1 is the scores, choice 2 is the fastest times
    choice = 0

    try:
        j = pygame.joystick.Joystick(0)
        j.init()
        controller = True
    except:
        controller = False

    while True:
        #Change the leaderboard being seen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    channel2.play(pygame.mixer.Sound(menuNav))
                    choice += 1
                elif event.key == pygame.K_LEFT:
                    channel2.play(pygame.mixer.Sound(menuNav))
                    choice = choice - 1
                elif event.key == pygame.K_RSHIFT:
                    channel2.play(pygame.mixer.Sound(menuSelect))
                    return False
            if controller == True:
                dPad = j.get_hat(0)
                if dPad == (1,0):
                    channel2.play(pygame.mixer.Sound(menuNav))
                    choice += 1
                elif dPad == (-1,0):
                    channel2.play(pygame.mixer.Sound(menuNav))
                    choice = choice - 1
                elif j.get_button(1):
                    channel2.play(pygame.mixer.Sound(menuSelect))
                    return False

        #format the window
        window.fill((36,63,93))
        if choice % 2 == 0:
            temp = scores
        else:
            temp = times

        buttonB = text_format('O or Right Shift - Back', 'Calibri.ttf', 40, white)
        #header initial positions
        names_x = 50
        headers_x = 300
        headers_y = 50

        for i in range(0, len(temp)):
            name = text_format(temp[i][0], 'Calibri.ttf', 40, white)
            value = text_format(temp[i][1], 'Calibri.ttf', 40, white)
            ranking = text_format(str(i), 'Calibri.ttf', 40, white)
            names_rect = name.get_rect()
            values_rect = value.get_rect()
            window.blit(name , (names_x, headers_y))
            window.blit(value, (headers_x, headers_y))
            if i > 0:
                window.blit(ranking, (names_x - 30, headers_y))
            headers_y = headers_y + 50

        buttonBRect = buttonB.get_rect()
        window.blit(buttonB, (displayWidth / 1.05 - (buttonBRect[2]), 640))
        pygame.display.update()
        clock.tick(60)
