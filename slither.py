import pygame
import time
from settings import *
import random

#ucitava sve module iz pygamea i pygame zvuka
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

#Definiramo FPS, default font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

#Radimo custom boju pomocu rgba i alphe(transparentnosti,opcionalno)
#         R    G    B
white = (255, 255, 255)
green = (0, 155, 0)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (0, 255, 255)

#postavljamo nas display i njegovu velicinu
GameDisplay = pygame.display.set_mode((display_width, display_height))

#ovdje dodajemo title
pygame.display.set_caption(name)

#ovdje definiramo sve spriteove koje ucitavamo
img = pygame.image.load('snakehead.png')
apple = pygame.image.load('apple.png')

#a ovdje sve zvukove
bite_sound = pygame.mixer.Sound("bite.wav")

def score(msg, color, x, y):
    screen_text = font.render(msg, True, color)
    GameDisplay.blit(screen_text, [x, y])
    pygame.display.update()

def snake(block_size, snakelist):

    #rotira sliku
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    #dodaje sliku od zmijine glave u listu za crtanje(umjesto kvadrata)
    GameDisplay.blit(head, (snakelist[-1][0], snakelist[-1] [1]))

    for XnY in snakelist[:-1]:
        pygame.draw.rect(GameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

# PORUKE
#game over poruka
game_over = "Game over! press C to play again or press Q to exit!"

#funkcije za poruke

def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (display_width/2), (display_height/2)
    GameDisplay.blit(textSurf, textRect)
    pygame.display.update()


def GameLoop():
    #OSTALE VARIJABLE
    global direction

    # VARIJABLE ZA LOKACIJU
    GameExit = False
    GameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0
    #lista za zmiju je van while petlje, kako bi se zmija mogla povecati
    snakelist = []
    snakelength = 1

    #BOUNDRIES
    left_boundry = 780-block_size
    right_boundry = 10+block_size
    upper_boundry = 60 + block_size
    lower_boundry = 590-block_size

    #x i y lokacija jabuke, round radimo da dobijemo broj djeljiv s 10, posto nam je velicina ekrana i zmije djeljiva s 10
    randAppleX = round(random.randrange(right_boundry, left_boundry))
    randAppleY = round(random.randrange(upper_boundry, lower_boundry)) #/10.0)*10.0

    #dok je vrijednost gameexita false
    while not GameExit:

        #provjerava je li gameover true i radi sljedece radnje
        while GameOver == True:
            GameDisplay.fill(white)
            message_to_screen(game_over, red)
            pygame.display.update()

            #funkcija za ponovnu igru
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameExit = True
                    GameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        GameExit = True
                        GameOver = False
                    if event.key == pygame.K_c:
                        GameLoop()

        for event in pygame.event.get():
            #ako pritisnemo x, izlazimo iz igrice
            if event.type == pygame.QUIT:
                GameExit = True
            #ako pritsnemo tipku, pomjeramo se u tom smjeru za odreden broj pixela
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"

        # provjerava je li zmija dosla do granice igre
        if lead_x >= 780-block_size or lead_x <=10+block_size or lead_y <= 60+block_size or lead_y >= 590-block_size:
            GameOver = True

        #updateamo varijablu lead_x
        lead_x += lead_x_change
        lead_y += lead_y_change

        GameDisplay.fill(white)

        GameDisplay.blit(apple, (randAppleX, randAppleY))

        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)

        #sprjecava zmiju da se povecava ako nismo pojeli jabuku
        if len(snakelist) > snakelength:
            del snakelist[0]

        #ako bilo koji dio tijela ima istu lokaciju kao snake head, igra faila
        for eachsegment in snakelist[:-1]:
            if eachsegment == snakehead:
                time.sleep(1)
                GameOver = True

        snake(block_size, snakelist)

        #Granice igrice
        pygame.draw.rect(GameDisplay, black, (790, 80, 10, 520))
        pygame.draw.rect(GameDisplay, black, (0, 590, 800, 10))
        pygame.draw.rect(GameDisplay, black, (0, 80, 10, 520))
        pygame.draw.rect(GameDisplay, black, (0, 70, 800, 10))

        #ScoreText
        score = f"Score: {snakelength}"
        screen_text = font.render(score, True, green)
        GameDisplay.blit(screen_text, [10, 10])

        pygame.display.update()

        #COLISION SA JABUKOM
        if lead_x > randAppleX and lead_x < randAppleX + apple_size or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_size:
            if lead_y > randAppleY and lead_y < randAppleY + apple_size:
                randAppleX = round(random.randrange(right_boundry, left_boundry)) #/10.0)*10.0
                randAppleY = round(random.randrange(upper_boundry, lower_boundry)) #/10.0)*10.0
                snakelength += 1
                pygame.mixer.Sound.play(bite_sound)
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_size:
                randAppleX = round(random.randrange(right_boundry, left_boundry)) #/10.0)*10.0
                randAppleY = round(random.randrange(upper_boundry, lower_boundry)) #/10.0)*10.0
                snakelength += 1
                pygame.mixer.Sound.play(bite_sound)

        clock.tick(FPS)


    #ponistava pygame.init i mixer.init
    pygame.mixer.quit()
    pygame.quit()
    #izlazi iz igrice
    quit()

GameLoop()
