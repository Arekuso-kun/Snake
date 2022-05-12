import random
import pygame
import pyrebase

pygame.init()  # now use display and fonts

RESOLUTION = (800, 600)
DISPLAY = pygame.display.set_mode((RESOLUTION))
WIDTH = DISPLAY.get_width()
HEIGHT = DISPLAY.get_height()

pygame.display.set_caption("Snake")

# database
firebaseConfig = {
  'apiKey': "AIzaSyCBEDJOVt__ItEoPYMjm5hSWKP4CGD6f1I",
  'authDomain': "snakeproject-37e7f.firebaseapp.com",
  'projectId': "snakeproject-37e7f",
  'storageBucket': "snakeproject-37e7f.appspot.com",
  'messagingSenderId': "122025097488",
  'appId': "1:122025097488:web:74b6116afe574b5ab3cd95",
  'measurementId': "G-LSXLDR8XJ5",
  'databaseURL':"https://snakeproject-37e7f-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# end_database

clock = pygame.time.Clock()
timer_event = pygame.USEREVENT + 1
clock_event = pygame.USEREVENT + 2
pygame.time.set_timer(timer_event, 125) # 1000 = 1s
pygame.time.set_timer(clock_event, 1000) # 1000 = 1s

WHITE = {0:("#000000"),
         10:("#1a1a1a"),
         20:("#333333"),
         30:("#4d4d4d"),
         40:("#666666"),
         50:("#808080"),
         60:("#999999"),
         70:("#b3b3b3"),
         80:("#cccccc"),
         90:("#e6e6e6"),
         100:("#ffffff")}

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_RED = (255,170,170)
LIGHT_GREEN = (170,255,170)
LIGHT_BLUE = (170,170,255)

def font_c_size(size):
    return pygame.font.Font('fonts/SnakeChan-YdV8.ttf', size)

SQUARE_DIM = 12
PLAY_FIELD_DIRECTION = [[0 for i in range(0,42)] for j in range(0,42)]
PLAY_FIELD_STATUS = [[0 for i in range(0,42)] for j in range(0,42)]
for i in range(0,42):
    for j in range(0,42):
        if i == 0 or i == 41 or j == 0 or j == 41:
            PLAY_FIELD_STATUS[i][j] = 1
SNAKE_HEAD = {"x": random.randrange(1, 40), "y": random.randrange(1, 40)}
PLAY_FIELD_STATUS[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 1
SNAKE_TAIL = {"x": SNAKE_HEAD['x'], "y": SNAKE_HEAD['y']}
FOOD = {"x": random.randrange(1, 40), "y": random.randrange(1, 40)}

move_up = False
move_down = False
move_left = False
move_right = False
next_move = False

main_menu_screen = True
insert_username_screen = False
game_start = False
game_over_var = False
f = open("data\high_score.txt", "rt")
high_score = int(f.read())
f.close()
score = 0
time = 0
clock_start = False
clock_sec = 0
clock_min = 0
clock_hour = 0

movement = 0.0
movement_up = True
movement_value = 0.0

leaderbord_show = False

username = ''



def movement_valuef(num):
    return -(num**2)/40

button_restart = [SQUARE_DIM + SQUARE_DIM*42/2 - SQUARE_DIM*20/2, HEIGHT - SQUARE_DIM*20, SQUARE_DIM*20, SQUARE_DIM*10]

def draw_square(x, y, color, border_val):
    pygame.draw.rect(DISPLAY, color, [SQUARE_DIM + SQUARE_DIM*x, HEIGHT - SQUARE_DIM*2 - SQUARE_DIM*y, SQUARE_DIM, SQUARE_DIM], border_radius=border_val)

def game_over():
    global game_over_var
    if PLAY_FIELD_STATUS[SNAKE_HEAD['x']][SNAKE_HEAD['y']] == 1:
        game_over_var = True
    else:
        PLAY_FIELD_STATUS[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 1

def draw_button(button, SURFACE, str):
    color_hover = WHITE[80]
    color = WHITE[90]
    color_boder = WHITE[60]
    color_boder_hover = WHITE[50]
    if button[0] <= mouse_x <= button[0]+button[2] and button[1] <= mouse_y <= button[1]+button[3]:
        pygame.draw.rect(SURFACE, color_hover, button, width=0, border_radius=10)
        pygame.draw.rect(SURFACE, color_boder_hover, button, width=2, border_radius=10)
    else:
        pygame.draw.rect(SURFACE, color, button, width=0, border_radius=10)
        pygame.draw.rect(SURFACE, color_boder, button, width=2, border_radius=10)
    text = font_c_size(32).render(str, True, WHITE[10])
    SURFACE.blit(text, (button[0] + button[2]/2 - text.get_width()/2, button[1] + button[3]/2 - text.get_height()/2))


def pressed_button(button):
    if button[0] <= mouse_x <= button[0]+button[2] and button[1] <= mouse_y <= button[1]+button[3]:
        return True

pause = False
running = True

while running:  # main game loop

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if pressed_button(button_restart) and game_over_var == True:
                PLAY_FIELD_DIRECTION = [[0 for i in range(0,42)] for j in range(0,42)]
                PLAY_FIELD_STATUS = [[0 for i in range(0,42)] for j in range(0,42)]
                for i in range(0,42):
                    for j in range(0,42):
                        if i == 0 or i == 41 or j == 0 or j == 41:
                            PLAY_FIELD_STATUS[i][j] = 1
                SNAKE_HEAD = {"x": random.randrange(1, 40), "y": random.randrange(1, 40)}
                PLAY_FIELD_STATUS[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 1
                SNAKE_TAIL = {"x": SNAKE_HEAD['x'], "y": SNAKE_HEAD['y']}
                FOOD = {"x": random.randrange(1, 40), "y": random.randrange(1, 40)}
                
                move_up = False
                move_down = False
                move_left = False
                move_right = False

                game_over_var = False
                score = 0
                time = 0
                clock_start = False
                clock_sec = 0
                clock_min = 0
                clock_hour = 0

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN and main_menu_screen == True:
                insert_username_screen = True
                main_menu_screen = False

            if insert_username_screen == True:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                if event.unicode.isalnum():
                    username += event.unicode
                if event.key == pygame.K_RETURN and len(username)>1:
                    insert_username_screen = False
                    game_start = True

            if game_start == True:

                if event.key == pygame.K_p:
                    if pause == False:
                        pause = True
                    else:
                        pause = False

                if event.key == pygame.K_l:
                    if leaderbord_show == True:
                        leaderbord_show = False
                    else:
                        leaderbord_show = True

                if pause == False:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and move_down == False and next_move == False:
                        move_down = move_left = move_right = False
                        move_up = True
                        next_move = True
                        clock_start = True
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and move_right == False and next_move == False:
                        move_up = move_down = move_right = False
                        move_left = True
                        next_move = True
                        clock_start = True
                    if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and move_up == False and next_move == False:
                        move_up = move_left = move_right = False
                        move_down = True
                        next_move = True
                        clock_start = True
                    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and move_left == False and next_move == False:
                        move_up = move_down = move_left = False
                        move_right = True
                        next_move = True
                        clock_start = True

        if game_start == True:

            if pause == False:
                if event.type == clock_event and game_over_var == False and clock_start == True:
                    clock_sec += 1
                    if clock_sec == 60:
                        clock_min += 1
                        clock_sec = 0

                if event.type == timer_event and game_over_var == False:
                    next_move = False
                    if move_up == True:
                        PLAY_FIELD_DIRECTION[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 1
                        SNAKE_HEAD['y'] += 1
                        game_over()

                    elif move_left == True:
                        PLAY_FIELD_DIRECTION[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 2
                        SNAKE_HEAD['x'] -= 1
                        game_over()

                    elif move_down == True:
                        PLAY_FIELD_DIRECTION[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 3
                        SNAKE_HEAD['y'] -= 1
                        game_over()

                    elif move_right == True:
                        PLAY_FIELD_DIRECTION[SNAKE_HEAD['x']][SNAKE_HEAD['y']] = 4
                        SNAKE_HEAD['x'] += 1
                        game_over()

                    if not(SNAKE_HEAD['x'] == FOOD['x'] and SNAKE_HEAD['y'] == FOOD['y']) and game_over_var == False:
                        if PLAY_FIELD_DIRECTION[SNAKE_TAIL['x']][SNAKE_TAIL['y']] == 1:
                            PLAY_FIELD_STATUS[SNAKE_TAIL['x']][SNAKE_TAIL['y']] = 0
                            SNAKE_TAIL['y'] += 1
                            
                        elif PLAY_FIELD_DIRECTION[SNAKE_TAIL['x']][SNAKE_TAIL['y']] == 2:
                            PLAY_FIELD_STATUS[SNAKE_TAIL['x']][SNAKE_TAIL['y']] = 0
                            SNAKE_TAIL['x'] -= 1

                        elif PLAY_FIELD_DIRECTION[SNAKE_TAIL['x']][SNAKE_TAIL['y']] == 3:
                            PLAY_FIELD_STATUS[SNAKE_TAIL['x']][SNAKE_TAIL['y']] = 0
                            SNAKE_TAIL['y'] -= 1

                        elif PLAY_FIELD_DIRECTION[SNAKE_TAIL['x']][SNAKE_TAIL['y']] == 4:
                            PLAY_FIELD_STATUS[SNAKE_TAIL['x']][SNAKE_TAIL['y']] = 0
                            SNAKE_TAIL['x'] += 1
                    elif game_over_var == False:
                        FOOD = {"x": random.randrange(1, 40), "y": random.randrange(1, 40)}
                        score += 1
                        if high_score < score:
                            high_score = score

    DISPLAY.fill(WHITE[20])

    (mouse_x, mouse_y) = pygame.mouse.get_pos()

    if insert_username_screen == True:
        text_name = font_c_size(46).render("Insert player name", True, WHITE[90])
        DISPLAY.blit(text_name, (WIDTH/2 - text_name.get_width()/2, HEIGHT/3 - text_name.get_height()))
        text_username = font_c_size(32).render(username, True, WHITE[90])
        DISPLAY.blit(text_username, (WIDTH/2 - text_username.get_width()/2, HEIGHT/2))

    if game_start == True:
        text_mini_title = font_c_size(64).render("Snake", True, WHITE[90])
        DISPLAY.blit(text_mini_title, (SQUARE_DIM + SQUARE_DIM*42/2 - text_mini_title.get_width()/2, SQUARE_DIM*2.25))
        pygame.draw.rect(DISPLAY, WHITE[20], [SQUARE_DIM, HEIGHT - SQUARE_DIM*43, SQUARE_DIM*42, SQUARE_DIM*42], border_radius=3)
        pygame.draw.rect(DISPLAY, WHITE[30], [SQUARE_DIM*2, HEIGHT - SQUARE_DIM*42, SQUARE_DIM*40, SQUARE_DIM*40], border_radius=3)
        pygame.draw.rect(DISPLAY, WHITE[50], [SQUARE_DIM, HEIGHT - SQUARE_DIM*43, SQUARE_DIM*42, SQUARE_DIM*42], border_radius=3, width=1)
        pygame.draw.rect(DISPLAY, WHITE[50], [SQUARE_DIM*2, HEIGHT - SQUARE_DIM*42, SQUARE_DIM*40, SQUARE_DIM*40], border_radius=3, width=1)
        draw_square(FOOD['x'], FOOD['y'], LIGHT_BLUE, 6)

        for i in range(1,41):
            for j in range(1,41):
                if PLAY_FIELD_STATUS[i][j] == 1:
                    draw_square(i, j, LIGHT_RED, 3)

        text_leaderboard = font_c_size(16).render("Press L for leaderboard", True, WHITE[90])
        DISPLAY.blit(text_leaderboard, (WIDTH - SQUARE_DIM - text_leaderboard.get_width(), SQUARE_DIM))
        text_pause = font_c_size(16).render("Press P to pause", True, WHITE[90])
        DISPLAY.blit(text_pause, (WIDTH - SQUARE_DIM - text_pause.get_width(), SQUARE_DIM*2 + text_pause.get_height()))

        text_score = font_c_size(32).render("High Score", True, WHITE[90])
        DISPLAY.blit(text_score, (WIDTH - SQUARE_DIM*22, SQUARE_DIM*10))
        text_score = font_c_size(32).render(" " + str(high_score), True, WHITE[90])
        DISPLAY.blit(text_score, (WIDTH - SQUARE_DIM*22, SQUARE_DIM*14))

        text_score = font_c_size(32).render("Score", True, WHITE[90])
        DISPLAY.blit(text_score, (WIDTH - SQUARE_DIM*22, SQUARE_DIM*20))
        text_score = font_c_size(32).render(" " + str(score), True, WHITE[90])
        DISPLAY.blit(text_score, (WIDTH - SQUARE_DIM*22, SQUARE_DIM*24))

        text_clock = font_c_size(32).render("Time", True, WHITE[90])
        DISPLAY.blit(text_clock, (WIDTH - SQUARE_DIM*22, SQUARE_DIM*30))
        text_clock = font_c_size(32).render(" " + str("{:02d}".format(clock_min)) + ":" + str("{:02d}".format(clock_sec)), True, WHITE[90])
        DISPLAY.blit(text_clock, (WIDTH - SQUARE_DIM*22, SQUARE_DIM*34))

        if pause == True:
            text_pause = font_c_size(32).render("Paused", True, WHITE[90])
            DISPLAY.blit(text_pause, (SQUARE_DIM + SQUARE_DIM*42/2 - text_pause.get_width()/2, HEIGHT - SQUARE_DIM*42/1.5 - text_pause.get_height()/2))

        if game_over_var == True:
            draw_button(button_restart, DISPLAY, "RESTART")
            f_read = open("data/high_score.txt", "r+")
            if high_score > int(f_read.read()):
                f_write = open("data/high_score.txt", "w+")
                f_write.write(str(high_score))
                data = {"player": username, "score": high_score, "time_sec": clock_sec, "time_min": clock_min}
                db.child("leaderboard").push(data)
            f_read.close()
            f_write.close()

        if leaderbord_show == True:
            pygame.draw.rect(DISPLAY, WHITE[20], [0, 0, WIDTH, HEIGHT])
            text_lb = font_c_size(64).render("Leaderboard", True, WHITE[90])
            DISPLAY.blit(text_lb, (WIDTH/2 - text_lb.get_width()/2, SQUARE_DIM*2.25))
            players = db.child("leaderboard").order_by_child("score").get()
            space = 0
            player_list = []
            for player in players.each():
                player_list.insert(0, player.val())
            for player in player_list:
                text_score = font_c_size(16).render(str(int(space/50 + 1)) + ".\t Name: " + str(player['player']) + "\t Score: " + str(player['score']) + "\t Time: "  + str("{:02d}".format(player['time_min'])) + ":"  + str("{:02d}".format(player['time_sec'])), True, WHITE[90])
                DISPLAY.blit(text_score, (WIDTH/2 - text_score.get_width()/2, SQUARE_DIM*15.25 + space))
                space += 50

    if main_menu_screen == True:
        text_title = font_c_size(128).render("Snake", True, WHITE[90])
        if movement_up == True:
            movement -= 1
            movement_value = movement_valuef(movement)
            if movement < -20:
                movement_up = False
        else:
            movement += 1
            movement_value = movement_valuef(movement)
            if movement > 20:
                movement_up = True
        DISPLAY.blit(text_title, (WIDTH/2 - text_title.get_width()/2, HEIGHT/2 - text_title.get_height()/2 - movement_value))
        text_sub_title = font_c_size(32).render("Press Enter to start...", True, WHITE[90])
        DISPLAY.blit(text_sub_title, (WIDTH/2 - text_sub_title.get_width()/2, HEIGHT/1.25 - text_sub_title.get_height()/2))

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
