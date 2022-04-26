''' Importing Libraries '''
import pygame, random, time, math, sys
from csv import reader, writer

''' Starting Modules '''
pygame.init()
pygame.font.init()

''' Global Variables '''
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
turns = 0

''' Window Settings '''
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris Hard Mode')

''' Dimension Reference '''
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - (1.05*play_height)

''' Colours '''
#              R   G   B
cyan =      ( 14,246,238) #I Piece
blue =      (  0,  2,230) #J Piece
orange =    (226,161, 35) #L Piece 
yellow =    (245,251, 24) #O Piece
green =     ( 42,233, 31) #S Piece
purple =    (226, 34,217) #T Piece
red =       (216, 11, 26) #Z Piece

''' SHAPE FORMATS '''
S = [['.....',
      '.....',
      '..00..',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#Shape arrays
shapes = [S, Z, I, O, J, L, T]
database = []
shape_colours = [green, red, cyan, yellow, blue, orange, purple]
# index 0 - 6 represent shape

''' Piece Class '''
class Piece(object):
    def __init__(self,x,y,shape):
        self.x = x                                          #Piece X Coordinate
        self.y = y                                          #Piece y Coordinate
        self.shape = shape                                  #Shape layout
        self.colour = shape_colours[shapes.index(shape)]    #Colour of the shape
        self.rotation = 0                                   #Rotation shape

''' Game Functions '''

#Create Grid Array for Python
def create_grid(locked_pos={}):
    #Generate Grid Arrays
    grid = [[(0,0,0)for x in range(10)] for x in range(20)]
    #Locked Positions for Pieces
    for i in range(len(grid)):         #Loop for making a grid
        for j in range(len(grid[i])):
            if (j,i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    #Returns Grid 
    return grid

#Checks if the piece can be placed on the grid
def valid_space(shape, grid):
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    #asigning positions to the piece
    formatted = convert_shape_format(shape)
    #checking if the piece is in a valid space or not
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

#Checking if the Piece is on the grid or not
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

'''Reload Bag'''
def reload(pieces, bag, size):
    #Previous states
    pieces = [S, Z, I, O, J, L, T]
    bag = pieces
    size = 6
    return pieces, bag, size

'''gen algorithm 2'''
def gen2(bag, size):
    #Randomly pick from the bag
    pick = random.randint(0, size)
    choice = bag[pick]
    #Remove the item chosen
    del bag[pick]
    size = size - 1
    return Piece(5,0, choice), size

''' Graphic Functions '''

#Make it visible to us
def convert_shape_format(shape):
    positions = []    #Makes list for the positions of the peice
    layout = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(layout):
        row = list(line)
        for j, column in enumerate(row):
            #Would return the position as filled if block had piece in it
            if column == '0':
                positions.append((shape.x + j,shape.y + i)) #The positions when being used by python

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) #The positions when being refereneced
        
    return positions

#Drawing Text in the middle of the screen for the lose message
def draw_text_middle(surface, text, size, colour):
    #Font to use
    font = pygame.font.SysFont('calibri', size, bold = True)
    label = font.render(text, 1, colour)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

def draw_high_score_mess(surface, text, size, colour):
    #Font to use
    font = pygame.font.SysFont('calibri', size, bold = True)
    label = font.render(text, 1, colour)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 80 + top_left_y + play_height/2 - label.get_height()/2))

#Draw the grid on the pygame window to make the pieces look like series of blocks  
def draw_grid(surface, grid):
    #Taking the window references
    sx = top_left_x
    sy = top_left_y
    #Drawing the lines
    for i in range(len(grid)):
        #The Horizontal Lines
        pygame.draw.line(surface, (128,128,128), (sx, sy + i* block_size), (sx+play_width, sy + i* block_size))
        #The Vertical Lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))

#Clearing rows on the grid
def clear_rows(grid, locked):
    #Amount of lines cleared
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        #If the colour of the grid is not black
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    #Moving all the pieces on the grid down
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)  #Locks the pieces in place
    return inc
        
#Drawing the Next shape that will appear
def draw_next_shape(shape1, shape2, shape3, shape4, surface):
    #Font
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('Next Shapes', 1, (255,255,255))
    #Positioning where to place the piece
    sx = top_left_x + play_width + 30 
    sy = top_left_y + play_height/2 - 275
    layout1 = shape1.shape[shape1.rotation % len(shape1.shape)]   #Shape 1
    layout2 = shape2.shape[shape2.rotation % len(shape2.shape)]   #Shape 2
    layout3 = shape3.shape[shape3.rotation % len(shape3.shape)]   #Shape 3
    try:
        layout4 = shape4.shape[shape4.rotation % len(shape4.shape)]   #Shape 4
    except:
        pass
    #Needed to be able to display Piece 1
    for i, line in enumerate(layout1):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape1.colour, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    #Piece 2
    for i, line in enumerate(layout2):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape2.colour, (sx + j*block_size, (sy + i*block_size + 150), block_size, block_size), 0)
    #Piece 3
    for i, line in enumerate(layout3):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape3.colour, (sx + j*block_size, (sy + i*block_size + 300), block_size, block_size), 0)

    #Piece being held
    try:
        sx = top_left_x + play_width + 30
        for i, line in enumerate(layout4):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape4.colour, (sx + j*block_size - 560, (sy + i * block_size + 325), block_size, block_size), 0)
    except:
        pass

    #Drawing the label
    surface.blit(label, (sx + 4, sy - 25 ))       
    
#Changing the highest score on the external file
def update_score(database,name, nscore):
    #check if the database needs to be updated
    for i in range(0, len(database)):
        #sort the list and remove items if there are more than 5
        if nscore > int(database[i][1]):
            database.insert(i,[name, nscore])
            break
    if len(database) == 0:
        database.append([name, nscore])
    elif len(database) > 5:
        database = database[0:5]

    #Write the csv file back
    with open('infinite.csv', 'w', newline='') as file:
        score_writer = writer(file)
        score_writer.writerows(database)

#opens the file with the highest score
def max_score():
    score = 0
    name = ''
    datbase = [[name, score]]
    try:
        with open('infinite.csv', 'r') as file:
            #database = [[name, score]]
            database = list(reader(file))
            for i in range(0,len(database)):
                if score < int(database[i][1]):
                    score = int(database[i][1])
                    name = database[i][0]
    except:
        f = open('sprint.csv','x')
        f.close()
    return database,name, score

#Drawing the window to play the game
def draw_window(surface, grid, score, level, last_score, total_lines):
    #Filling in the surface
    surface.fill((36,63,93))
    #The level the player is on
    font = pygame.font.SysFont('calibri', 50)
    label = font.render(('Level:' + str(level)), 1, (255,255,255))
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 20))
    # Current Score
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('Score: ', 1, (255,255,255))
    #Positioning the scores properly
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height/2 - 300
    surface.blit(label, (sx - 560, sy + 100))
    # Score Number
    label = font.render(str(score), 1, (255,255,255))
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height/2 - 270
    surface.blit(label, (sx - 560, sy + 100))
    # High Score
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('High Score:', 1, (255,255,255))
    #Positioning the scores properly
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height/2 - 300
    surface.blit(label, (sx - 560, sy))
    #High Score Number:
    label = font.render(str(last_score), 1, (255,255,255))
    sx = top_left_x + play_width + 30 
    sy = top_left_y + play_height/2 - 270
    surface.blit(label, (sx - 560, sy))
    # Total Lines
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('Lines: ', 1, (255,255,255))
    #Positioning the amount of lines cleared
    sx = top_left_x + play_width + 30 
    sy = top_left_y + play_height/2 - 300
    surface.blit(label, (sx - 560, sy + 200))
    #Lines number
    label = font.render(str(total_lines), 1, (255,255,255))
    sx = top_left_x + play_width + 30 
    sy = top_left_y + play_height/2 - 270
    surface.blit(label, (sx - 560, sy + 200))
    #Piece being held info
    label = font.render("Hold:", 1, (255,255,255))
    surface.blit(label, (sx - 560, sy + 300))
    #Drawing the Pieces on the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    #Drawing the boarder of the grid
    pygame.draw.rect(surface, (255,255,255), (top_left_x, top_left_y, play_width, play_height), 7)
    #Drawing the grid
    draw_grid(surface, grid)
    
'''The Pause Section'''
#Making the Text visible forthe pause screen
def makeTextObjs(text, font, colour):
    surf = font.render(text, True, colour)
    return surf, surf.get_rect()
#Closing the game
def terminate():
    pygame.quit()
    sys.exit()
#Closing the screen throughthe main options
def checkForQuit():
    for event in pygame.event.get(pygame.QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(pygame.KEYUP): # get all the KEYUP events
        if event.key == pygame.K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
        if event.type == pygame.KEYDOWN:
            continue
        #If a key was pressed it would send the key input
        return event.key
    #If no key was pressed, no events would be returned
    return None

# Same as check for key but for the buttons
def checkForButtonPress():
    try:
        j = pygame.joystick.Joystick(0)
        j.init()
        checkForQuit()
        for event in pygame.event.get([pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]):
            if event.type == pygame.JOYBUTTONDOWN:
                continue
            return True
        return None
    except:
        pass

#The Pause Function itself, taking the pause state and the text it needs to display
def pause_func(text, pause_state, controller_state):
    while pause_state == True:
        # Font to use in the screen
        font = pygame.font.SysFont('calibri', 50)
        # Draw the text
        titleSurf, titleRect = makeTextObjs(text, font, (255,255,255))
        titleRect.center = (int(s_width / 2) - 3, int(s_height / 2) - 3)
        win.blit(titleSurf, titleRect)
        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = makeTextObjs('Press any key or button to continue.', font, (255,255,255))
        pressKeyRect.center = (int(s_width / 2), int(s_height / 2) + 100)
        win.blit(pressKeySurf, pressKeyRect)
        # Checks if a key was pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.quit()
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                pause_state = False
            #First checks if the controller is connected
            if controller_state == True:
                if event.type == pygame.JOYBUTTONDOWN:
                    pause_state = False
        #Will enter this section to update screen if controller is connected
        if controller_state == True:
            while (checkForButtonPress() == None):
                pygame.display.update()
                clock = pygame.time.Clock()
                clock.tick(60)
                # Testing purposes
                break
        #No controller
        elif controller_state == False:
            #Updates the screen whilst no other key was pressed
            while (checkForKeyPress() == None) :
                pygame.display.update()
                clock = pygame.time.Clock()
                clock.tick(60)
                # Testing purposes
                break

''''''''''''

#Allowing the user to enter their name for the high score
def enter_name(window):
    font = pygame.font.SysFont('calibri', 50, bold=False)
    user_text = ''
    #the first two is the position of the box
    input_rect = pygame.Rect(100,200, 140, 50)
    white = (255,255,255)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                #Where the Name can be returned
                elif event.key == pygame.K_RETURN:
                    return user_text
                elif len(user_text) == 20:
                    continue
                else:
                    user_text += event.unicode
        window.fill((36, 63, 93))
        pygame.draw.rect(window, white, input_rect, 2)

        text_surface = font.render(user_text, 1, white)
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        label = font.render("Enter Your Name:", 1, white)
        window.blit(label, (input_rect.x, input_rect.y - 50))

        input_rect.w = max(100,text_surface.get_width() + 25)
        pygame.display.update()
        clock.tick(60)

''' The main Game Code '''
def infinite(win):
    ''' Audio Files '''
    #BGM
    startMusic = 'audio files/Music/game-start1.ogg'                #Music between levels 1 - 4 (theme = 0)
    midMusic = 'audio files/Music/game-mid1.ogg'                    #Music between levels 5 - 9 (theme = 1)
    finalMusic = 'audio files/Music/game-last1.ogg'                 #Music between levels 10 and up (theme = 2)
    #Sound effects
    lineClear = 'audio files/Sound Effects/Line Clear.ogg'          #Effect when line is cleared
    tetrisClear = 'audio files/Sound Effects/Tetris Clear.ogg'      #Effect when 4 lines are cleared
    levelClear = 'audio files/Sound Effects/Level Up.ogg'           #Effect when player goes up a level
    hardDrop = 'audio files/Sound Effects/Hard Drop.ogg'            #Effect when hard drop is performed
    gameOver = 'audio files/Sound Effects/game-over.ogg'            #Effect when the game over condition is met
    #For new algorithm
    shapes = [S, Z, I, O, J, L, T]
    holder = None
    tempBag = shapes
    size = 6 #The amount of pieces dropped without an I piece
    #Scores, grid positons
    database, name, last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    #Starting the Audio Service
    pygame.mixer.init()
    channel1 = pygame.mixer.Channel(0) #Background Music
    channel2 = pygame.mixer.Channel(1) #Sound Effects
    #System variables
    change_piece = False
    run = True
    #Fetching the pieces
    current_piece, size = gen2(tempBag, size)
    next_piece, size = gen2(tempBag, size)
    next1_piece, size = gen2(tempBag, size)
    next2_piece, size = gen2(tempBag, size)
    #checking how long it takes to drop the piece
    clock = pygame.time.Clock()    
    #Game Variables for the piece
    fall_time = 0            #time taken for the piece to fall
    fall_speed = 0.26        #The speed at which the piece falls
    store_speed = float(0)   #The variable of the speed when the game is paused
    score = 0                #The score
    level = 1                #The level
    total_lines = 0          #The total amount of lines cleared
    store_x = 0              #The variable for storing the x position of the piece
    store_y = 0              #The variable for storing the y position of the piece
    store_rotation = 0       #The variable for stroing the rotation state of the piece
    lines_to_clear = 10      #The amount of lines needed to clear to level up
    #Game Variables for specific mechanics
    hard_drop = False          #allows the piece the drop immediately
    soft_drop = False          #allows the piece to drop faster
    change_fall_speed = False  #allows the hard drop and soft drop to be performed
    controller = False         #variable for controller
    pause = False              #Allows the game to be paused if true
    changeMusic = False        #Allows the BGM to be changed
    buffer = False             #Allows the game to delay between the pause menu and the game
    highScoreMet = False       #Allows the high score to be visually changed
    switch = True
    theme = 0                  #Allows the BGM to be changed specifically
    #Background Music (Bug on not changing themes)
    channel1.play(pygame.mixer.Sound(startMusic),-1)
    #Checking if the Controller is connected or not
    try:
        j = pygame.joystick.Joystick(0)
        j.init()
        #Test Mesasge
        #Allows the code to run specific code for the controller
        controller = True
    except:
        #Test Message
        pass
    #While the game is running
    while run:
        if buffer == True:
            time.sleep(3)
            buffer = False
        #Background Music Fix
        if level >= 5 and level < 10 and theme == 0:          #Change to the 2nd bgm theme
            theme = 1
            changeMusic = True                                #Validation to make sure that it should change bgms
        if level >= 10 and theme == 1:                        #Change to the 3rd bgm theme
            theme = 2
            changeMusic = True
        if theme == 1 and changeMusic == True:                #Changing bgms
            channel1.play(pygame.mixer.Sound(midMusic),-1)
            changeMusic = False
        if theme == 2 and changeMusic == True:
            channel1.play(pygame.mixer.Sound(finalMusic), 1)
            changeMusic = False
        #Gets the grid
        grid = create_grid(locked_positions)
        #If the piece is still falling or not
        fall_time += clock.get_rawtime()
        clock.tick(60)
        #If the Piece is on the bottom
        if fall_time/1000 > fall_speed:
            fall_time = 0
            #Move piece down
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                #Goes back up
                current_piece.y -= 1
                change_piece = True
        #Checking for specific inputs from the user
        for event in pygame.event.get():
            #If the user wants to quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.quit()
                pygame.display.quit()
            ''' Keyboard Controls '''
            if event.type == pygame.KEYDOWN:
                #Arrow Key Left (move left)
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                #Arrow Key Right (move right)
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                #Space (Drop Hard)
                if event.key == pygame.K_SPACE:
                    #Temporarely makes the fall speed almost instantaneous
                    store_speed = fall_speed
                    fall_speed = 0
                    hard_drop = True
                #Arrow Key Down (Drop Soft)
                if event.key == pygame.K_DOWN:
                    #Temporarely makes the fall speed faster
                    store_speed = fall_speed
                    fall_speed = round(store_speed/5,2)
                    soft_drop = True
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                #Z Key (rotate CCW)
                if event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                    current_piece.rotation -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation += 1
                #X Key (rotate CW)
                if event.key == pygame.K_x or event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                #c key (Hold Piece)
                if (event.key == pygame.K_c or event.key == pygame.K_LSHIFT) and switch == True:
                    current_piece.x = 5
                    current_piece.y = 0
                    if holder == None:
                        holder = current_piece
                        current_piece = next_piece
                        next_piece = next1_piece
                        next1_piece = next2_piece
                        next2_piece, size = gen2(tempBag, size)
                    else:
                        memory = holder
                        holder = current_piece
                        current_piece = memory
                    switch = False
                #P Key, pausing the game
                if event.key == pygame.K_p:
                    #Makes a new window
                    win.fill((36,63,93))
                    #Stores the previous location and fall speed of the pieces
                    store_x = current_piece.x
                    store_y = current_piece.y
                    store_speed = fall_speed
                    store_rotation = current_piece.rotation
                    #Makes the Piece never fall to the bottom
                    fall_speed = math.inf
                    pause = True
                    #Pauses the bgm
                    channel1.pause()
                    pause_func('Paused', pause, controller)
                    buffer = True
                    #Resumes the bgm
                    channel1.unpause()
                    #Reloads the Position and fall speed back after pause
                    current_piece.x = store_x
                    current_piece.y = store_y
                    fall_speed = store_speed
            ''' Controller Controlls '''
            if controller == True:
                #Starts the D-Pad controls (only works here for some reason)
                dPad = j.get_hat(0)
                #D-Pad Down
                if dPad == (0,-1):
                    store_speed = fall_speed
                    fall_speed = round(store_speed/5,2)
                    soft_drop = True
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                #D-Pad Up        
                if dPad == (0, 1):
                    store_speed = fall_speed
                    fall_speed = round(store_speed/20,3)
                    hard_drop = True
                #D-Pad Right    
                if dPad == (1,0):
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                #D-Pad Left        
                if dPad == (-1,0):
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                #Controller buttons
                if event.type == pygame.JOYBUTTONDOWN:
                    #O button on controller (Playstation reference)
                    if j.get_button(1):
                        current_piece.rotation += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.rotation -= 1
                    #triangle On controller (Playstation reference)
                    if j.get_button(2):
                        current_piece.rotation -= 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.rotation += 1
                    if j.get_button(4) and switch == True:
                        current_piece.x = 5
                        current_piece.y = 0
                        if holder == None:
                            holder = current_piece
                            current_piece = next_piece
                            next_piece = next1_piece
                            next1_piece = next2_piece
                            next2_piece, size = gen2(tempBag, size)
                        else:
                            memory = holder
                            holder = current_piece
                            current_piece = memory
                        switch = False
                    if j.get_button(9):
                         #Makes a new window
                        win.fill((36,63,93))
                        #Stores the previous location and fall speed of the pieces
                        store_x = current_piece.x
                        store_y = current_piece.y
                        store_speed = fall_speed
                        store_rotation = current_piece.rotation
                        #Makes the Piece never fall to the bottom
                        fall_speed = math.inf
                        pause = True
                        channel1.pause()
                        pause_func('Paused', pause, controller)
                        buffer = True
                        channel1.unpause()
                        #Reloads the Position and fall speed back after pause
                        current_piece.x = store_x
                        current_piece.y = store_y
                        fall_speed = store_speed
            #If the Down button was pressed and then liffted up               
            if (event.type == pygame.KEYUP) or ((controller == True) and (dPad == (0,0))):
                if soft_drop == True:
                    soft_drop = False
                    #Fall Speed returns to before
                    fall_speed = store_speed
        #Gets the location of the current piece    
        shape_pos = convert_shape_format(current_piece)
        #Fills the grid with the colour of the piece
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.colour
        if buffer == True:
            time.sleep(3)
            buffer = False
        #If the piece needs to be changed
        if change_piece:
            #Delayed purposly
            time.sleep(0.01)
            #If the Up button was pressed
            if hard_drop == True:
                #Sound effect specific to the Hard Drop
                channel2.play(pygame.mixer.Sound(hardDrop))
                fall_speed = store_speed
                hard_drop = False
            #IF the down button was pressed
            #Split the two if's as it doesn't operate properly as wanted
            if (event.type == pygame.K_SPACE) or ((controller == True) and (dPad == (0,0))):
                if soft_drop == True:
                    soft_drop = False
                    fall_speed = store_speed
            #Fills the grid with the pieces already in the grid
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.colour
            #Changes the Pieces
            current_piece = next_piece
            next_piece = next1_piece
            next1_piece = next2_piece
            next2_piece, size = gen2(tempBag, size)
            switch = True
            #Reloading the bag
            if size < 0:
                shapes, tempBag, size = reload(shapes, tempBag, size)
            change_piece = False
            #Updating information
            lines_cleared = clear_rows(grid, locked_positions)
            total_lines += lines_cleared
            #Scoring the player depending on the amount of lines cleared
            if lines_cleared == 1:      #One line Cleared
                score += (level * 100)
                channel2.play(pygame.mixer.Sound(lineClear))
                time.sleep(0.01)
            elif lines_cleared == 2:    #Two Lines cleared
                score += (level * 250)
                channel2.play(pygame.mixer.Sound(lineClear))
                time.sleep(0.01)
            elif lines_cleared == 3:    #Three Lines Cleared
                score += (level * 400)
                channel2.play(pygame.mixer.Sound(lineClear))
                time.sleep(0.01)
            elif lines_cleared == 4:    #Four Lines Cleared
                score += (level * 800)
                channel2.play(pygame.mixer.Sound(tetrisClear))
                time.sleep(0.01)
        #Changing the fall speed and level at depending on the amount of lines cleared (Bug present before, is now fixed)
        if total_lines > 0:
            if total_lines >= (level * lines_to_clear):          #If the amount of lines met were achieved
                level += 1
                channel2.play(pygame.mixer.Sound(levelClear))    #play sound effect
                change_fall_speed = True
        if change_fall_speed == True:
            for event in pygame.event.get():
                #Whenever the up button/key is pressed
                if (event.type == pygame.KEYUP) or ((controller == True) and (dPad == (0,0))):
                    if soft_drop == True:
                        soft_drop = False
                        #Fall Speed returns to before
                        fall_speed = store_speed
            fall_speed = round((fall_speed - 0.01),3)  #Makes it fall faster and rounds it to 3dp
            if fall_speed <= 0.05:                     #Setting the limit to the fall speed
                fall_speed = 0.05
            change_fall_speed = False                  #Stops the fall speed from changing
        if score > last_score:                         #Allows the high score to be updated
            highScoreMet = True
            last_score = score
        #Updating the Screen with the new information
        draw_window(win, grid, score, level, last_score, total_lines)
        draw_next_shape(next_piece, next1_piece, next2_piece,holder, win)
        pygame.display.update()
        #When Game over occurs
        if check_lost(locked_positions):
            channel1.play(pygame.mixer.Sound(gameOver))             #play game over sound
            draw_text_middle(win, 'You Lose', 60, (255,255,255))    #display message
            for i in range(0, len(database)):
                if score > int(database[i][1]):
                    highScoreMet = True
            if highScoreMet == True:
                draw_high_score_mess(win, """You're on the Leaderboard!""", 60, (255,255,255))
                pygame.display.update()
                pygame.time.delay(4000)
                #let the user enter their name
                name = enter_name(win)
            pygame.display.update()
            pygame.time.delay(4000)
            run = False                                             #Stops game
            update_score(database,name,score)                                     #Updates the score if higher or not
            pygame.mixer.quit()