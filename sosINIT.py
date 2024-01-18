import pygame
from pygame.locals import *

#Resolution
heigth = 600
width = 900

#Game Setting
squareSize = 70

#Colours
GREY = (70, 70, 70)
BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255,140,0)
GREEN = (50, 70, 50)
YELLOW = (255, 100, 0)

#Initialize
pygame.init()

#Font
logoFont = pygame.font.Font('font/solid.ttf', 100)
sbuttonFont = pygame.font.Font('font/solid.ttf', 50)
mbuttonFont = pygame.font.Font('font/solid.ttf', 20)
boardFont = pygame.font.Font('font/Washington.ttf', 24)
scoreFont = pygame.font.Font('font/Washington.ttf', 48)
score1Font = pygame.font.Font('font/Digit.TTF', 48)
playerFont = pygame.font.Font('font/Washington.ttf', 48)
cellFont = pygame.font.Font('font/Washington.ttf', 50)
sizeUpButton = pygame.font.Font('font/Digit.TTf',48)
sizeDownButton = pygame.font.Font('font/Digit.TTf',48)

#Text
logoText = logoFont.render('S O S', True, BLUE)
sbuttonText = sbuttonFont.render('SIMPLE', True, BLACK)
sbuttonhoverText = sbuttonFont.render('SIMPLE', True, ORANGE)
mbuttonText = mbuttonFont.render('GENERAL', True, BLACK)
mbuttonhoverText = mbuttonFont.render('GENERAL', True, ORANGE)
boardText = boardFont.render('S | O', True, ORANGE)
bscoreText = scoreFont.render('Blue:', True, BLUE)
rscoreText = scoreFont.render('Red:', True, RED)
player1onText = playerFont.render('<--', True, BLUE)
player2onText = playerFont.render('<--', True, RED)
playeroffText = playerFont.render('<--', True, GREY)
