import pygame, time, math

from infinite import *

#to load the times back into the database, stopwatch in terms of milliseconds
def update_times(database, name, stopwatch):
    #check if the database needs to be updated
    for i in range(0, len(database)):
        if stopwatch < int(database[i][1]):
            database.insert(i, [name, stopwatch])
            break
    if len(database) == 0:
        database.append([name, stopwatch])
    elif len(database) > 5:
        database = database[0:5]

    with open('sprint.csv', 'w', newline='') as file:
        time_writer = writer(file)
        time_writer.writerows(database)

#load the database and load the shortest time in seconds to be displayed
def import_times():
    shortest_time = 10000000
    name = ''
    database = [[name, shortest_time]]
    try:
        with open('sprint.csv', 'r') as file:
            #formated as database = [[name, milliseconds]]
            database = list(reader(file))
            for i in range(0, len(database)):
                if shortest_time > int(database[i][1]):
                    shortest_time = int(database[i][1])
                    name = database[i][0]
    except:
        f = open('sprint.csv','x')
        f.close()

    return database, name, shortest_time

#need to change to fastest time
#score not needed
def draw_window1(surface, grid, level, last_time, total_lines, stopwatch):
    # Filling in the surface
    surface.fill((36, 63, 93))
    # The level the player is on
    font = pygame.font.SysFont('calibri', 50)
    label = font.render(('Level:' + str(level)), 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 20))
    # Current Score
    font = pygame.font.SysFont('calibri', 30)
    label = font.render("Time: {}".format(stopwatch), 1, (255, 255, 255))
    # Positioning the scores properly
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height / 2 - 300
    surface.blit(label, (sx - 560, sy + 100))
    # Fastest Time
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('Fastest Time:', 1, (255, 255, 255))
    # Positioning the time properly
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height / 2 - 300
    surface.blit(label, (sx - 560, sy))
    # Fastest Time number:
    minutes, seconds = timer(last_time)
    if seconds < 10.0:
        last_time = "{0}:0{1}".format(minutes, seconds)
    else:
        last_time = "{0}:{1}".format(minutes, seconds)
    label = font.render(str(last_time), 1, (255, 255, 255))
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height / 2 - 270
    surface.blit(label, (sx - 560, sy))
    # Total Lines
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('Lines: ', 1, (255, 255, 255))
    # Positioning the amount of lines cleared
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height / 2 - 300
    surface.blit(label, (sx - 560, sy + 200))
    # Lines number
    label = font.render(str(total_lines), 1, (255, 255, 255))
    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height / 2 - 270
    surface.blit(label, (sx - 560, sy + 200))
    # Piece being held info
    label = font.render("Hold:", 1, (255, 255, 255))
    surface.blit(label, (sx - 560, sy + 300))
    # Drawing the Pieces on the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    # Drawing the boarder of the grid
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height), 7)
    # Drawing the grid
    draw_grid(surface, grid)

def timer(milliseconds):
    seconds = round(milliseconds / 1000, 2)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    return round(int(minutes)), round(seconds, 2)

# opens the file with the highest score
def shortest_time():
    with open('sprint.csv', 'r') as f:
        lines = f.readlines()
        time_taken = lines[0].strip()
    return time_taken

def sprint(win):
    ''' Audio Files '''
    # BGM
    startMusic = 'audio files/Music/game-start1.ogg'  # Music between levels 1 - 4 (theme = 0)
    # Sound effects
    lineClear = 'audio files/Sound Effects/Line Clear.ogg'  # Effect when line is cleared
    tetrisClear = 'audio files/Sound Effects/Tetris Clear.ogg'  # Effect when 4 lines are cleared
    levelClear = 'audio files/Sound Effects/Level Up.ogg'  # Effect when player goes up a level
    hardDrop = 'audio files/Sound Effects/Hard Drop.ogg'  # Effect when hard drop is performed
    gameOver = 'audio files/Sound Effects/game-over.ogg'  # Effect when the game over condition is met
    # For new algorithm
    shapes = [S, Z, I, O, J, L, T]
    holder = None
    tempBag = shapes
    size = 6  # The amount of pieces dropped without an I piece
    # Scores, grid positons
    database, name, last_time = import_times()
    locked_positions = {}
    grid = create_grid(locked_positions)
    # Starting the Audio Service
    pygame.mixer.init()
    channel1 = pygame.mixer.Channel(0)  # Background Music
    channel2 = pygame.mixer.Channel(1)  # Sound Effects
    # System variables
    change_piece = False
    run = True
    # Fetching the pieces
    current_piece, size = gen2(tempBag, size)
    next_piece, size = gen2(tempBag, size)
    next1_piece, size = gen2(tempBag, size)
    next2_piece, size = gen2(tempBag, size)
    # checking how long it takes to drop the piece
    clock = pygame.time.Clock()
    # Game Variables for the piece
    fall_time = 0  # time taken for the piece to fall
    fall_speed = 0.26  # The speed at which the piece falls
    store_speed = float(0)  # The variable of the speed when the game is paused
    score = 0  # The score
    level = 1  # The level
    total_lines = 0  # The total amount of lines cleared
    store_x = 0  # The variable for storing the x position of the piece
    store_y = 0  # The variable for storing the y position of the piece
    store_rotation = 0  # The variable for stroing the rotation state of the piece
    lines_to_clear = 10  # The amount of lines needed to clear to level up
    milliseconds = 0
    # Game Variables for specific mechanics
    hard_drop = False  # allows the piece the drop immediately
    soft_drop = False  # allows the piece to drop faster
    change_fall_speed = False  # allows the hard drop and soft drop to be performed
    controller = False  # variable for controller
    pause = False  # Allows the game to be paused if true
    buffer = False  # Allows the game to delay between the pause menu and the game
    highScoreMet = False  # Allows the high score to be visually changed
    switch = True
    # Background Music (Bug on not changing themes)
    channel1.play(pygame.mixer.Sound(startMusic), -1)
    # Checking if the Controller is connected or not
    try:
        j = pygame.joystick.Joystick(0)
        j.init()
        # Test Mesasge
        # Allows the code to run specific code for the controller
        controller = True
    except:
        # Test Message
        pass
    # While the game is running
    while run:
        if buffer == True:
            time.sleep(3)
            buffer = False
        # Gets the grid
        grid = create_grid(locked_positions)
        # If the piece is still falling or not
        fall_time += clock.get_rawtime()
        milliseconds += clock.get_rawtime()
        clock.tick(60)
        # If the Piece is on the bottom
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            # Move piece down
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                # Goes back up
                current_piece.y -= 1
                change_piece = True
        # Checking for specific inputs from the user
        for event in pygame.event.get():
            # If the user wants to quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.quit()
                pygame.display.quit()
            ''' Keyboard Controls '''
            if event.type == pygame.KEYDOWN:
                # Arrow Key Left (move left)
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                # Arrow Key Right (move right)
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                # Space (Drop Hard)
                if event.key == pygame.K_SPACE:
                    # Temporarely makes the fall speed almost instantaneous
                    store_speed = fall_speed
                    fall_speed = 0
                    hard_drop = True
                # Arrow Key Down (Drop Soft)
                if event.key == pygame.K_DOWN:
                    # Temporarely makes the fall speed faster
                    store_speed = fall_speed
                    fall_speed = round(store_speed / 5, 2)
                    soft_drop = True
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                # Z Key (rotate CCW)
                if event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                    current_piece.rotation -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation += 1
                # X Key (rotate CW)
                if event.key == pygame.K_x or event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                # c key (Hold Piece)
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
                # P Key, pausing the game
                if event.key == pygame.K_p:
                    # Makes a new window
                    win.fill((36, 63, 93))
                    # Stores the previous location and fall speed of the pieces
                    store_x = current_piece.x
                    store_y = current_piece.y
                    store_speed = fall_speed
                    store_rotation = current_piece.rotation
                    # Makes the Piece never fall to the bottom
                    fall_speed = math.inf
                    pause = True
                    # Pauses the bgm
                    channel1.pause()
                    pause_func('Paused', pause, controller)
                    buffer = True
                    # Resumes the bgm
                    channel1.unpause()
                    # Reloads the Position and fall speed back after pause
                    current_piece.x = store_x
                    current_piece.y = store_y
                    fall_speed = store_speed
            ''' Controller Controlls '''
            if controller == True:
                # Starts the D-Pad controls (only works here for some reason)
                dPad = j.get_hat(0)
                # D-Pad Down
                if dPad == (0, -1):
                    store_speed = fall_speed
                    fall_speed = round(store_speed / 5, 2)
                    soft_drop = True
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                # D-Pad Up
                if dPad == (0, 1):
                    store_speed = fall_speed
                    fall_speed = round(store_speed / 20, 3)
                    hard_drop = True
                # D-Pad Right
                if dPad == (1, 0):
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                # D-Pad Left
                if dPad == (-1, 0):
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                # Controller buttons
                if event.type == pygame.JOYBUTTONDOWN:
                    # O button on controller (Playstation reference)
                    if j.get_button(1):
                        current_piece.rotation += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.rotation -= 1
                    # triangle On controller (Playstation reference)
                    if j.get_button(2):
                        current_piece.rotation -= 1
                        if not (valid_space(current_piece, grid)):
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
                        # Makes a new window
                        win.fill((36, 63, 93))
                        # Stores the previous location and fall speed of the pieces
                        store_x = current_piece.x
                        store_y = current_piece.y
                        store_speed = fall_speed
                        store_rotation = current_piece.rotation
                        # Makes the Piece never fall to the bottom
                        fall_speed = math.inf
                        pause = True
                        channel1.pause()
                        pause_func('Paused', pause, controller)
                        buffer = True
                        channel1.unpause()
                        # Reloads the Position and fall speed back after pause
                        current_piece.x = store_x
                        current_piece.y = store_y
                        fall_speed = store_speed
            # If the Down button was pressed and then liffted up
            if (event.type == pygame.KEYUP) or ((controller == True) and (dPad == (0, 0))):
                if soft_drop == True:
                    soft_drop = False
                    # Fall Speed returns to before
                    fall_speed = store_speed
        # Gets the location of the current piece
        shape_pos = convert_shape_format(current_piece)
        # Fills the grid with the colour of the piece
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.colour
        if buffer == True:
            time.sleep(3)
            buffer = False
        # If the piece needs to be changed
        if change_piece:
            # Delayed purposly
            time.sleep(0.01)
            # If the Up button was pressed
            if hard_drop == True:
                # Sound effect specific to the Hard Drop
                channel2.play(pygame.mixer.Sound(hardDrop))
                fall_speed = store_speed
                hard_drop = False
            # IF the down button was pressed
            # Split the two if's as it doesn't operate properly as wanted
            if (event.type == pygame.K_SPACE) or ((controller == True) and (dPad == (0, 0))):
                if soft_drop == True:
                    soft_drop = False
                    fall_speed = store_speed
            # Fills the grid with the pieces already in the grid
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.colour
            # Changes the Pieces
            current_piece = next_piece
            next_piece = next1_piece
            next1_piece = next2_piece
            next2_piece, size = gen2(tempBag, size)
            switch = True
            # Reloading the bag
            if size < 0:
                shapes, tempBag, size = reload(shapes, tempBag, size)
            change_piece = False
            # Updating information
            lines_cleared = clear_rows(grid, locked_positions)
            total_lines += lines_cleared
            # Scoring the player= depending on the amount of lines cleared
            if lines_cleared == 1:  # One line Cleared
                channel2.play(pygame.mixer.Sound(lineClear))
                time.sleep(0.01)
            elif lines_cleared == 2:  # Two Lines cleared
                channel2.play(pygame.mixer.Sound(lineClear))
                time.sleep(0.01)
            elif lines_cleared == 3:  # Three Lines Cleared
                channel2.play(pygame.mixer.Sound(lineClear))
                time.sleep(0.01)
            elif lines_cleared == 4:  # Four Lines Cleared
                channel2.play(pygame.mixer.Sound(tetrisClear))
                time.sleep(0.01)
        # Changing the fall speed and level at depending on the amount of lines cleared (Bug present before, is now fixed)
        if total_lines > 0:
            if total_lines >= (level * lines_to_clear):  # If the amount of lines met were achieved
                level += 1
                channel2.play(pygame.mixer.Sound(levelClear))  # play sound effect
                change_fall_speed = True
        if change_fall_speed == True:
            for event in pygame.event.get():
                # Whenever the up button/key is pressed
                if (event.type == pygame.KEYUP) or ((controller == True) and (dPad == (0, 0))):
                    if soft_drop == True:
                        soft_drop = False
                        # Fall Speed returns to before
                        fall_speed = store_speed
            fall_speed = round((fall_speed - 0.01), 3)  # Makes it fall faster and rounds it to 3dp
            if fall_speed <= 0.05:  # Setting the limit to the fall speed
                fall_speed = 0.05
            change_fall_speed = False  # Stops the fall speed from changing
        minutes, seconds = timer(milliseconds)
        if seconds < 10:
            stopwatch = "{0}:0{1}".format(minutes, seconds)
        else:
            stopwatch = "{0}:{1}".format(minutes, seconds)
        # Updating the Screen with the new information
        draw_window1(win, grid, level, last_time, total_lines, stopwatch)
        draw_next_shape(next_piece, next1_piece, next2_piece, holder, win)
        pygame.display.update()
        # When Game over occurs
        if check_lost(locked_positions):
            channel1.play(pygame.mixer.Sound(gameOver))  # play game over sound
            draw_text_middle(win, 'You Lose', 60, (255, 255, 255))  # display message
            pygame.display.update()
            pygame.time.delay(4000)
            run = False  # Stops game
            pygame.mixer.quit()
        elif total_lines >= 40:
            channel1.play(pygame.mixer.Sound(gameOver))  # play game over sound
            draw_text_middle(win, 'Sprint Complete', 80, (255, 255, 255))  # display message
            for i in range(0, len(database)):
                if milliseconds < last_time:
                    draw_high_score_mess(win, """You're on the Leaderboard!""", 60, (255, 255, 255))
                    pygame.display.update()
                    pygame.time.delay(4000)
                    name = enter_name(win)
                    break
            pygame.display.update()
            pygame.time.delay(4000)
            run = False  # Stops game
            update_times(database, name, milliseconds)  # Updates the score if higher or not
            pygame.mixer.quit()