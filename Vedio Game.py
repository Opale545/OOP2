import pygame
from settings import *
from ball3 import *
from ball2 import *

pygame.init()
#Decideds the screen dimension
screen = pygame.display.set_mode((screen_width, screen_height))
#Imports graphics of the games
background_image = pygame.image.load("Graphics/Background/Background.png").convert()
goal_left = pygame.image.load("Graphics/Background/Goal_left.png").convert_alpha()
goal_right = pygame.image.load("Graphics/Background/Goal_right.png").convert_alpha()# Load the goal image with alpha transparency
player_1 = pygame.image.load("Graphics/Player/Players1.png").convert_alpha()
player_2 = pygame.image.load("Graphics/Player/Players2.png").convert_alpha()
ball = pygame.image.load("Graphics/Ball/Ball pixel.png").convert_alpha()
pygame.display.set_caption("Black Window")

#Imports sound of the game of the games
cheering_sound = pygame.mixer.Sound("Sound/Effect/cheering.wav")
grunt_sound = pygame.mixer.Sound("Sound/Effect/hit.wav")

#Starts the game clock
clock = pygame.time.Clock()
#determins the ball staring positions
ball_pos = [560, 200]

#The score variable get determined
home_score = 0
away_score = 0
#The Phont of the scoreboard is established
score_font = pygame.font.Font(None, 36)

# Update the scoreboard

#Variables for who is kicking, starts of as both are False
player1_kick = False
player2_kick = False

#Other starting variables are set
is_falling = False
gravity = 10
ball_gravity = 5
ball_speed = 10
time = 0
time2 = 0
time3 = 0
last_kick = None
running = True


#Begins to run the code
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    #makes the players
    player_1_rect = pygame.Rect(player_1_pos[0], player_1_pos[1], player_1.get_width(), player_1.get_height())
    player_2_rect = pygame.Rect(player_2_pos[0], player_2_pos[1], player_2.get_width(), player_2.get_height())
    ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], ball.get_width(), ball.get_height())


    #Determines the two radius of the players
    player_1_radius = player_1.get_width() / 2
    player_2_radius = player_2.get_width() / 2
    #Calculates the distance beetween the two players
    distance = ((player_1_pos[0] - player_2_pos[0])**2 + (player_1_pos[1] - player_2_pos[1])**2)**0.5 + 70


    #Command that record key presses
    keys = pygame.key.get_pressed()

    # Move player 1 based on the WASD keys
    if keys[pygame.K_a]:
        player_1_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_1_pos[0] += player_speed
    if keys[pygame.K_w] and not is_jumping and not is_falling:
        is_jumping = True
        is_falling = False


    # Move player 2 based on the arrow keys
    if keys[pygame.K_LEFT]:
        player_2_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_2_pos[0] += player_speed
    if keys[pygame.K_UP] and not is_jumping2 and not is_falling2:
        is_jumping2 = True
        is_falling2 = False

    #if the player1 is jumping it makes the player move up
    if is_jumping:
        if jump_counter < jump_height:
            player_1_pos[1] -= jump_speed
            jump_counter += jump_speed
        else:
            is_jumping = False
            is_falling = True
            jump_counter = 0
    #If player1 is falling it will apply gravity onto the player until it reaches the floor
    elif is_falling:
        if player_1_pos[1] < 530:
            player_1_pos[1] += gravity
        else:
            is_falling = False

    #if the player1 is jumping it makes the player move up
    if is_jumping2:
        if jump2_counter < jump2_height:
            player_2_pos[1] -= jump2_speed
            jump2_counter += jump2_speed
        else:
            is_jumping2 = False
            is_falling2 = True
            jump2_counter = 0
    #If player1 is falling it will apply gravity onto the player until it reaches the floor
    elif is_falling2:
        if player_2_pos[1] < 530:
            player_2_pos[1] += gravity
        else:
            is_falling2 = False

    #Works out if the distance beetween the two players is smaller than the playersd radius
    if distance <= player_1_radius + player_2_radius:
        # Adjust the positions of the two players so they don't overlap
        if player_1_pos[0] < player_2_pos[0]:
            player_1_pos[0] -= player_speed
            player_2_pos[0] += player_speed
        else:
            player_1_pos[0] += player_speed
            player_2_pos[0] -= player_speed


    if player_1_rect.colliderect(ball_rect):
        # Player 1 hit the ball
        print("Player 1 hit the ball!")
        player1_kick = True
        player2_kick = False
        last_kick = 1
        grunt_sound.play()



    elif player_2_rect.colliderect(ball_rect):
        # Player 2 hit the ball
        print("Player 2 hit the ball!")
        player2_kick = True
        player1_kick = False
        last_kick = 2
        grunt_sound.play()


    #Starts timer that since a ball was last kicked
    if player1_kick == True or player2_kick == True:
        if time < 40:
            time += 1
        else:
            #After timer is up it resets timer, and states no one is currently kicking the ball since the timer
            time = 0
            player1_kick = False
            player2_kick = False

    #Makes the ball move up and to the right if player1 kicked the ball
    if player1_kick == True:
        ball_pos[0] += ball_speed
        ball_pos[1] -= 2

    #Makes the ball move up and to the left if player2 kicked the ball
    if player2_kick == True:
        ball_pos[0] -= ball_speed
        ball_pos[1] -= 2

    #sees if no one kicked the ball
    if player1_kick == False and player2_kick == False:
        #If player1 last kicked gracity is aplied to the ball, whilst still moving to the right
        if last_kick == 1:
            ball_pos[0] += ball_speed - 2
            ball_pos[1] += ball_gravity

        #If player1 last kicked gracity is aplied to the ball, whilst still moving to the left
        if last_kick == 2:
            ball_pos[0] -= ball_speed - 2
            ball_pos[1] += ball_gravity

        #Usually only aplied at the start of a game or at a restart and the ball just drops down.
        else:
            ball_pos[1] += ball_gravity

    #calculates if the ball is going out of bounds (screen)
    if ball_pos[0] <= 0 or ball_pos[0] >= screen_width - ball.get_width():
        # Reverse the horizontal velocity to bounce off the vertical walls
        if time3 < 20:
            ball_speed = -ball_speed
            time3 += 1
            last_kick = None
        else:
            ball_speed = 10
            time3 = 0

    #Calculates if the ball is inside the left goal
    if ball_pos[1] > 460 and ball_pos[0] < 70:
        print("goal for player 2")
        cheering_sound.play()

        #restart stuff
        ball_pos = [560, 200]
        player1_kick = False
        player2_kick = False
        last_kick = None
        ball_speed = 10
        is_jumping2 = False
        jump2_counter = 0
        player_2_pos = [900, 530]
        is_falling2 = False
        jump_height = 200
        jump_speed = 15
        is_jumping = False
        jump_counter = 0
        player_1_pos = [120, 530]
        player_speed = 5
        away_score += 1







    #Calculates if the ball is inside the right goal
    if ball_pos[1] > 360 and ball_pos[0] > 1090:
        print("goal for player 1")
        cheering_sound.play()

        #restart stuff
        ball_pos = [560, 200]
        player1_kick = False
        player2_kick = False
        last_kick = None
        ball_speed = 10
        is_jumping2 = False
        jump2_counter = 0
        player_2_pos = [900, 530]
        is_falling2 = False
        jump_height = 200
        jump_speed = 15
        is_jumping = False
        jump_counter = 0
        player_1_pos = [120, 530]
        player_speed = 5
        home_score += 1

    #Works if the ball is above the goal and try's to make it bounce of
    if ball_pos[1] < 460 and ball_pos[0] < 70:
        last_kick = 1
        ball_pos[0] += 70
        ball_pos[1] -= 30

    if ball_pos[1] < 460 and ball_pos[0] > 1090:
        ball_pos[0] -= 70
        ball_pos[1] -= 30

    #Works out if the ball is on the floor
    if ball_pos[1] > 630:
        #if it is on the floor it stops gravity
        ball_gravity = 0
    else:
        ball_gravity = 4

    #TOP SECRET GOD MODE
    if keys[pygame.K_g] and keys[pygame.K_f]:
        jump_height = 400
        jump_speed = 25
        player_speed = 100
        home_score += 10000000000000000000000
        away_score -= 99


    if player_1_pos[0] < 0:
        player_1_pos[0] = 0
    elif player_1_pos[0] > screen_width - player_1.get_width():
        player_1_pos[0] = screen_width - player_1.get_width()

    # Restrict player 2 within the screen boundaries
    if player_2_pos[0] < 0:
        player_2_pos[0] = 0
    elif player_2_pos[0] > screen_width - player_2.get_width():
        player_2_pos[0] = screen_width - player_2.get_width()


    print(last_kick)


    # Blit the goal image onto the screen surface at position (50, 100)
    screen.blit(background_image, (0, 0))



    #Draws the score board
    score_text = f"Home: {home_score}  Away: {away_score}"
    score_surface = score_font.render(score_text, True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    #Draws evreything else on the screen
    screen.blit(ball, ball_pos)
    screen.blit(player_1, player_1_pos)
    screen.blit(player_2, player_2_pos)
    screen.blit(goal_left, (-80, 430))
    screen.blit(goal_right, (1000, 430))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()



