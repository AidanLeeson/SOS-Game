import pygame
from pygame.locals import *
from sosGame import *
from sosINIT import *



def menu():
    player1_type = "Human"
    player2_type = "Human"
    pygame.init()
    mySurface = pygame.display.set_mode((width, heigth))  # Corrected 'heigth' to 'height'
    pygame.display.set_caption('SOS')
    inProgress = True
    boardSize = 3
    sizeDisplayX, sizeDisplayY, sizeDisplayWidth, sizeDisplayHeight = 100, 200, 100, 50


    mySurface.fill(GREY)
    displayLogo(mySurface)
    player1_button_rect = pygame.Rect(600, 400, 150, 50)
    player2_button_rect = pygame.Rect(600, 460, 150, 50)
    
    while inProgress:
        drawButton(mySurface, BLACK, 0)
        drawBoardButton(mySurface, "Increase", 100, 50, 150, 50, YELLOW)
        drawBoardButton(mySurface, "Decrease", 100, 120, 150, 50, YELLOW)
        drawTogglePlayerButton(mySurface, player1_button_rect, player1_type)
        drawTogglePlayerButton(mySurface, player2_button_rect, player2_type)
        sizeText = sbuttonFont.render(str(boardSize), True, BLACK)
        mySurface.blit(sizeText, (100, 200))
        mouse = pygame.mouse.get_pos()

        displayBoardSize(mySurface, boardSize, sizeDisplayX, sizeDisplayY, sizeDisplayWidth, sizeDisplayHeight)
        
        if (380 + 150 > mouse[0] > 380) and (240 + 50 > mouse[1] > 240):
            drawButton(mySurface, YELLOW, 1)
        elif (380 + 150 > mouse[0] > 380) and (310 + 50 > mouse[1] > 310):
            drawButton(mySurface, YELLOW, 2)
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if (380 + 150 > mouse[0] > 380) and (240 + 50 > mouse[1] > 240):
                    gameloopSimple(boardSize, squareSize, player1_type, player2_type)
                    inProgress = False
                elif (380 + 150 > mouse[0] > 380) and (310 + 50 > mouse[1] > 310):
                    gameloopGeneral(boardSize, squareSize, player1_type, player2_type)
                    inProgress = False
                if player1_button_rect.collidepoint(mouse):
                    player1_type = "Computer" if player1_type == "Human" else "Human"
                elif player2_button_rect.collidepoint(mouse):
                    player2_type = "Computer" if player2_type == "Human" else "Human"
                if isButtonClicked(100, 50, 150, 50, mouse):
                    boardSize += 1
                    displayBoardSize(mySurface, boardSize, sizeDisplayX, sizeDisplayY, sizeDisplayWidth, sizeDisplayHeight)
                elif isButtonClicked(100, 120, 150, 50, mouse):
                    boardSize -= 1
                    displayBoardSize(mySurface, boardSize, sizeDisplayX, sizeDisplayY, sizeDisplayWidth, sizeDisplayHeight)


            if event.type == QUIT:
                inProgress = False

        pygame.display.update()  # Fixed indentation
    
    pygame.quit()
    return boardSize

def displayLogo(mySurface):
    textRect = logoText.get_rect()
    textRect.topleft = (320, 110)
    mySurface.blit(logoText, textRect)

def drawButton(mySurface, textColor, option):
    pygame.draw.rect(mySurface, WHITE, (380,240,150,50))
    pygame.draw.rect(mySurface, WHITE, (380,310,150,50))
    textRect = sbuttonText.get_rect()
    textRect.topleft = (386, 249)
    if option == 1:
        mySurface.blit(sbuttonhoverText, textRect)
    else:
        mySurface.blit(sbuttonText, textRect)
    
    textRect = mbuttonText.get_rect()
    textRect.topleft = (383, 328)
    if option == 2:
        mySurface.blit(mbuttonhoverText, textRect)
    else:
        mySurface.blit(mbuttonText, textRect)

def drawBoardButton(mySurface, text, x, y, width, height, color):
    pygame.draw.rect(mySurface, color, (x, y, width, height))
    buttonText = sbuttonFont.render(text, True, BLACK)  # Assuming BLACK is defined
    buttonTextRect = buttonText.get_rect(center=(x + width / 2, y + height / 2))
    mySurface.blit(buttonText, buttonTextRect)

def displayBoardSize(mySurface, boardSize, x, y, width, height):
    # Clear the previous number
    pygame.draw.rect(mySurface, GREY, (x, y, width, height))  # Assuming GREY is your background color

    # Render and display the new number
    sizeText = sbuttonFont.render(str(boardSize), True, BLACK)  # Assuming BLACK is defined
    textRect = sizeText.get_rect(center=(x + width / 2, y + height / 2))
    mySurface.blit(sizeText, textRect)

def drawTogglePlayerButton(surface, rect, player_type):
    pygame.draw.rect(surface, WHITE, rect)
    buttonText = sbuttonFont.render(player_type, True, BLACK)
    buttonTextRect = buttonText.get_rect(center=rect.center)
    surface.blit(buttonText, buttonTextRect)

menu()
