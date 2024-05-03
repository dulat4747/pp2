import pygame
import time
import random
import sys
import psycopg2

pygame.init()
# colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Basic sets
dis = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

# Initial length of a snake
snake_block = 10
level = 1
score = 0
p = 0

# font sets
font_style = pygame.font.SysFont("bahnschrift", 30)
font_style1 = pygame.font.SysFont("bahnschrift", 22)
font_style2 = pygame.font.SysFont("bahnschrift", 24)
score_font = pygame.font.SysFont("comicsansms", 25)
pause_font = pygame.font.SysFont("bahnschrift", 70)

# Score and Level message
def Your_score(score, level, lscore, llevel):
    value = score_font.render(" Your Score: " + str(score) + "  Level: " + str(level), True, yellow)
    value1 = score_font.render(" Last Score: " + str(int(lscore)) + "  Last Level: " + str(int(llevel)), True, yellow)
    dis.blit(value, [0, 0])
    dis.blit(value1, [0, 30])


# Draw a snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


# Message to User
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [200 / 6, 400 / 3])

def connect(info, username, score, level):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgres1",
            user="postgres",
            port="5432",
            password="Dulat2005")

        # Autocommit to database
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        if info == 0:
            cur.execute(f"""INSERT INTO public.score(
                        	username, user_score, user_level)
                    	VALUES ('{username}', {score}, {level});""")
        if info == 1:
            cur.execute(f"""UPDATE public.score
	                        SET user_score={score}, user_level={level}
	                        WHERE username='{username}';""")
        if info == 2:
            cur.execute(f"""SELECT * FROM score WHERE username = '{username}'""")
            return cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# The main game loop
def gameLoop():
    game_over = False
    game_close = False
    saved = False
    global score
    global level
    user_text = ''
    input_rect = pygame.Rect(165, 150, 140, 38)
    save_rect = pygame.Rect(270, 200, 80, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    color_i = (148, 60, 199)
    active = False

    while not saved:
        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                if save_rect.collidepoint(event.pos):
                    username = user_text
                    info = 0
                    if not username == '':
                        connect(info, username, score, level)
                        saved = True

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                    global p
                    p -= 8
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode
                    p += 7

        # it will set background color of screen
        dis.fill((0, 0, 0))

        if active:
            color_i = color_active
        else:
            color = color_passive

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(dis, color_i, input_rect)
        pygame.draw.rect(dis, color, save_rect)


        text_surface = font_style.render(user_text, True, (255, 255, 255))
        start_button = font_style1.render('START', True, (255, 255, 255))
        mess = font_style2.render('ENTER YOUR USERNAME', True, (255, 255, 255))
        # render at position stated in arguments
        dis.blit(text_surface, (300 - p, input_rect.y + 5))
        dis.blit(start_button, (278, 206))
        dis.blit(mess, (170, 110))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(280, text_surface.get_width() + 10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)

    # Initial position of a snake
    x1 = 600 / 2
    y1 = 400 / 2

    # Change in position
    x1_change = 0
    y1_change = 0

    # Speed, Length, level of a snake
    snake_speed = 10
    snake_List = []
    Length_of_snake = 1

    # Random position for the food
    foodx = round(random.randrange(0, 600 - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, 400 - snake_block) / 10.0) * 10.0
    food_start_time = pygame.time.get_ticks()


    while not game_over:
        # Level Increasing depending on length of a snake
        if Length_of_snake == 5:
            level = 2
            snake_speed = 12
        if Length_of_snake == 10:
            level = 3
            snake_speed = 15
        if Length_of_snake == 15:
            level = 4
            snake_speed = 17
        if Length_of_snake == 20:
            level = 5
            snake_speed = 19
        if Length_of_snake == 25:
            level = 6
            snake_speed = 21
        if Length_of_snake == 30:
            level = 7
            snake_speed = 23

        while game_close == True:
            info = 1
            connect(info,username,score,level)
            dis.fill(black)
            # Message to User if he lost the game
            message("You Lost! Press C-Play Again or Q-Quit", red)

            info = 2
            list1 = connect(info,username,score,level)
            if list1 is not None:
                Your_score(Length_of_snake - 1, level, list1[1], list1[2])
            else:
                print("No data found in the database for the user.")
            pygame.display.update()

            # Checking for keydown event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                # Pause in the game
                if event.key == pygame.K_SPACE:
                    pause = True
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                game_over = True
                                pause = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    pause = False
                        pygame.draw.circle(dis, (108, 59, 168), (300, 200), 50)
                        value3 = pause_font.render("II", True, white)
                        dis.blit(value3, [280, 170])
                        pygame.display.flip()


                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        # Checking for wall collision
        if x1 >= 600 or x1 < 0 or y1 >= 400 or y1 < 0:
            game_close = True
        # Position change
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        # Draw the food
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])

        # Snake movement
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Checking for collision of snake by himself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        score = Length_of_snake - 1
        info=2
        list1 = connect(info, username, score, level)
        if list1 is not None:
            Your_score(score, level, list1[1], list1[2])
        else:
            print("No data found in the database for the user.")

        pygame.display.update()
        # Checking for time limit for food
        if pygame.time.get_ticks() - food_start_time >= 4000:
            foodx = round(random.randrange(0, 600 - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, 400 - snake_block) / 10.0) * 10.0
            food_start_time = pygame.time.get_ticks()

        # Generating random position for food, so that it does not fall on a wall or a snake
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, 600 - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, 400 - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            food_start_time = pygame.time.get_ticks()

        clock.tick(snake_speed)
        if game_over == True:
            info = 1
            connect(info, username, score, level)

    pygame.quit()
    quit()


gameLoop()
