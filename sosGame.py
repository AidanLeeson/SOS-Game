import pygame
from pygame.locals import *
from sosAlgorithms import *
from sosINIT import *
from sosComp import *

def countPlayerPiecesInLine(line, board):
    player1_count, player2_count = 0, 0
    for (i, j) in line:
        if board[i][j] is not None:
            _, player = board[i][j]
            if player == 1:
                player1_count += 1
            elif player == 2:
                player2_count += 1
    print(f"Line: {line}, Player 1 Count: {player1_count}, Player 2 Count: {player2_count}")  # Debugging
    if player1_count > player2_count:
        return 1
    elif player2_count > player1_count:
        return 2
    else:
        return 0


def player_type(player,player1_type,player2_type):
    return player1_type if player == 1 else player2_type

def drawBoard(mySurface, n):
    x, y = 70, 70
    size = 70
    for i in range(n):
        for j in range(n):
            drawBoardCell(mySurface, WHITE, x + j * size, y + i * size, size)

def drawBoardCell(mySurface, COLOR, x, y, size):
    pos1 = (x, y)
    pos2 = (x + size, y)
    pos3 = (x + size, y + size)
    pos4 = (x, y + size)
    pygame.draw.line(mySurface, COLOR, pos1, pos2)
    pygame.draw.line(mySurface, COLOR, pos2, pos3)
    pygame.draw.line(mySurface, COLOR, pos3, pos4)
    pygame.draw.line(mySurface, COLOR, pos4, pos1)
    drawBoardLetter(mySurface, x, y, size)

def drawBoardLetter(mySurface, x, y, size):
    textRect = boardText.get_rect()
    textRect.topleft = (x, (y + 15))
    mySurface.blit(boardText, textRect)

def displayTeam(mySurface):
    textRect = bscoreText.get_rect()
    textRect.topleft = (600, 200)
    mySurface.blit(bscoreText, textRect)
    textRect.topleft = (600, 300)
    mySurface.blit(rscoreText, textRect)

def displayScore(mySurface, n, scores):
    clearScore(mySurface)
    player1str = str(scores[0])
    player2str = str(scores[1])
    player1 = score1Font.render(player1str, True, WHITE)
    player2 = score1Font.render(player2str, True, WHITE)
    textRect = player1.get_rect()
    textRect.topleft = (715, 190)
    mySurface.blit(player1, textRect)
    textRect.topleft = (715, 290)
    mySurface.blit(player2, textRect)

def clearScore(mySurface):
    rect = (715, 190, 70, 70)
    pygame.draw.rect(mySurface, GREY, rect)
    rect = (715, 290, 70, 70)
    pygame.draw.rect(mySurface, GREY, rect)

def displayPlayer(mySurface, n, player):
    if (player == 1):
        textRect = player1onText.get_rect()
        textRect.topleft = (800, 200)
        mySurface.blit(player1onText, textRect)
        textRect = playeroffText.get_rect()
        textRect.topleft = (800, 300)
        mySurface.blit(playeroffText, textRect)
    if (player == 2):
        textRect = playeroffText.get_rect()
        textRect.topleft = (800, 200)
        mySurface.blit(playeroffText, textRect)
        textRect = player2onText.get_rect()
        textRect.topleft = (800, 300)
        mySurface.blit(player2onText, textRect)


def clearCell(mySurface, board, i, j):
    x = 71 + (j * 70)
    y = 71 + (i * 70)
    rect = (x, y, 69, 69)
    pygame.draw.rect(mySurface, GREEN, rect)


def drawCell(mySurface, board, i, j):
    clearCell(mySurface, board, i, j)

    cell_content = board[i][j]
    if cell_content is not None:
        # Check if cell_content is a tuple (new format)
        if isinstance(cell_content, tuple):
            letter_value, player = cell_content
        else:
            # Handle integer values for backward compatibility
            letter_value = cell_content
            player = 1  # or some default player value

        letter = 'S' if letter_value == 1 else 'O'
        color = BLUE if player == 1 else RED

        x = 71 + (j * 70) + 20
        y = 71 + (i * 70) + 20
        text = cellFont.render(letter, True, color)
        textRect = text.get_rect()
        textRect.topleft = (x, y)
        mySurface.blit(text, textRect)


def drawLines(mySurface, line, player):
    # Check if line contains tuples of coordinates
    if line and isinstance(line[0], tuple):
        start_row, start_col = line[0]
        end_row, end_col = line[-1]

        # Calculate pixel coordinates and draw the line
        start_x = 70 + start_col * 70 + 35
        start_y = 70 + start_row * 70 + 35
        end_x = 70 + end_col * 70 + 35
        end_y = 70 + end_row * 70 + 35
        

        line_color = BLUE if player == 1 else RED
        pygame.draw.line(mySurface, line_color, (start_x, start_y), (end_x, end_y), 5)
    else:
        print("Invalid line format:", line)

        
def selectSquare(mySurface, board, n, size, player, chosen_letter):
    x = 70
    y = 70
    mouse = pygame.mouse.get_pos()

    for j in range(n):
        for i in range(n):
            square_rect = pygame.Rect(x + i * size, y + j * size, size, size)
            if square_rect.collidepoint(mouse) and possibleSquare(board, n, j, i):
                # Update the board with a tuple (letter, player)
                letter_value = 1 if chosen_letter == 'S' else 2
                board[j][i] = (letter_value, player)  # Use tuple (letter_value, player)
                return [i, j]
    return [-1, -1]

def determineLineWinner(line, board):
    player_contribution = {1: 0, 2: 0}

    for (i, j) in line:
        cell_content = board[i][j]
        if cell_content is not None:
            if isinstance(cell_content, tuple):
                _, player = cell_content
            else:
                # Handle integer values for backward compatibility
                player = 1 if cell_content == 1 else 2

            player_contribution[player] += 1

    # Determine the player with the maximum contribution
    max_contributions = max(player_contribution.values())
    winners = [player for player, contribution in player_contribution.items() if contribution == max_contributions]

    if len(winners) == 1:
        return winners[0]  # Return the single player who contributed the most
    else:
        return None  # In case of a tie, no winner is determined

def isBoardFull(board):
    return all(cell is not None for row in board for cell in row)

def displayWinnerMessage(mySurface, winner):
    message = f"Player {winner} wins!"
    message_font = pygame.font.Font(None, 36)  # Adjust font and size as needed
    message_text = message_font.render(message, True, (255, 255, 255))  # White color
    text_rect = message_text.get_rect(center=(width // 2, heigth // 2))
    mySurface.blit(message_text, text_rect)

def determineWinner(sos_scores):
    if sos_scores[0] > sos_scores[1]:
        return 1
    elif sos_scores[1] > sos_scores[0]:
        return 2
    else:
        return None  # Draw

def handleSOS(surface, board, n, sos_scores, total_sos_count, processed_sos):
    sos_lines = checkForSOS(board, n, processed_sos)
    if sos_lines:  # Check if sos_lines is not empty
        new_sos_lines = sos_lines

        for line_tuple in new_sos_lines:
            if len(line_tuple) == 2:  # Ensure the tuple has two elements
                line, player = line_tuple
                print(player)
                sos_scores[player - 1] += 1  # Correctly attribute the score to the right player
                if surface is not None:  # Only draw lines if surface is not None
                    drawLines(surface, line, player)
            else:
                print("Error: Invalid line tuple:", line_tuple)

        total_sos_count += len(new_sos_lines)
    return len(sos_lines)


def printBoard(board, file):
    for row in board:
        file.write(' '.join(str(cell) for cell in row) + '\n')



def gameloopSimple(n, size, player1_type, player2_type):
    f = open('GameOutput.txt','w')
    mySurface = pygame.display.set_mode((width, heigth))
    board = newBoard(n)
    pygame.display.set_caption('SOS')
    inProgress = True
    player = 1
    winning_score = 1
    current_letter = 'S'

    sos_scores = [0, 0]  # Initialize scores for both players
    total_sos_count = 0  # Initialize total SOS count
    processed_sos = []

    mySurface.fill(GREY)
    drawBoard(mySurface, n)
    displayTeam(mySurface)
    displayPlayer(mySurface, n, player)
    pygame.display.update()

    while inProgress:
        current_player_type = player_type(player, player1_type, player2_type)

        # AI's turn
        if current_player_type == "Computer":
            current_player_letter = 'S' if player == 1 else 'O'
            ai_move = computerMove(board, n, current_player_letter)
            if ai_move:
                i, j, ai_letter = ai_move
                letter_value = 1 if ai_letter == 'S' else 2
                board[i][j] = (letter_value, player) 
                drawCell(mySurface, board, i, j)  # Removed 'player' argument
                total_sos_count = handleSOS(mySurface, board, n, sos_scores, total_sos_count, processed_sos)
                if isBoardFull(board) or max(sos_scores) >= winning_score:
                        winning_player = sos_scores.index(max(sos_scores)) + 1
                        displayWinnerMessage(mySurface, winning_player)
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds to display the message
                        inProgress = False
                printBoard(board,f)
                f.write('Scores: Blue - ' + str(sos_scores[0]) + ' Red - ' + str(sos_scores[1]) + '\n' + '\n')
                player = 2 if player == 1 else 1
                f.write('Current Player: ' + str(player) + '\n')
            else:
                print("No valid move for Computer. Ending game.")
                break  # Exit the loop if no valid move
            
        # Human's turn
        for event in pygame.event.get():
            if current_player_type == "Human" and event.type == MOUSEBUTTONDOWN:
                position = selectSquare(mySurface, board, n, size, player, current_letter)
                if position[0] != -1:
                    letter_value = 1 if current_letter == 'S' else 2
                    board[position[1]][position[0]] = (letter_value, player)  # Update with tuple
                    drawCell(mySurface, board, position[1], position[0])
                    total_sos_count = handleSOS(mySurface, board, n, sos_scores, total_sos_count, processed_sos)
                    if isBoardFull(board) or max(sos_scores) >= winning_score:
                        winning_player = sos_scores.index(max(sos_scores)) + 1
                        displayWinnerMessage(mySurface, winning_player)
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds to display the message
                        inProgress = False
                printBoard(board,f)
                f.write('Scores: Blue - ' + str(sos_scores[0]) + ' Red - ' + str(sos_scores[1]) + '\n' + '\n')
                player = 2 if player == 1 else 1
                f.write('Current Player: ' + str(player) + '\n')

            elif event.type == KEYDOWN:
                if event.key == K_s:
                    current_letter = 'S'
                elif event.key == K_o:
                    current_letter = 'O'

            elif event.type == QUIT:
                inProgress = False

        displayPlayer(mySurface, n, player)
        pygame.display.update()

    pygame.quit()


def gameloopGeneral(n, size, player1_type, player2_type):
    f = open('GameOutput.txt','w')
    mySurface = pygame.display.set_mode((width, heigth))
    board = newBoard(n)
    pygame.display.set_caption('SOS')
    inProgress = True
    player = 1
    current_letter = 'S'

    sos_scores = [0, 0]  # Initialize scores for both players
    total_sos_count = 0  # Initialize total SOS count
    processed_sos = []

    mySurface.fill(GREY)
    drawBoard(mySurface, n)
    displayTeam(mySurface)
    displayPlayer(mySurface, n, player)
    pygame.display.update()

    while inProgress:
        current_player_type = player_type(player, player1_type, player2_type)

        # AI's turn
        if current_player_type == "Computer":
            current_player_letter = 'S' if player == 1 else 'O'
            ai_move = computerMove(board, n, current_letter)
            if ai_move:
                i, j, ai_letter = ai_move
                letter_value = 1 if ai_letter == 'S' else 2
                board[i][j] = (letter_value, player)  # Update the board with a tuple (letter, player)
                drawCell(mySurface, board, i, j)
                total_sos_count = handleSOS(mySurface, board, n, sos_scores, total_sos_count, processed_sos)
                if isBoardFull(board):
                        winning_player = determineWinner(sos_scores)
                        if winning_player:
                            displayWinnerMessage(mySurface, winning_player)
                            pygame.display.update()
                            pygame.time.wait(2000)  # Show message for 2 seconds
                            inProgress = False
                        else:
                            pygame.time.wait(2000)  # Show message for 2 seconds
                            inProgress = False
                printBoard(board,f)
                f.write('Scores: Blue - ' + str(sos_scores[0]) + ' Red - ' + str(sos_scores[1]) + '\n' + '\n')
                player = 2 if player == 1 else 1
                f.write('Current Player: ' + str(player) + '\n')


        # Human's turn
        for event in pygame.event.get():
            if current_player_type == "Human" and event.type == MOUSEBUTTONDOWN:
                position = selectSquare(mySurface, board, n, size, player, current_letter)
                if position[0] != -1:
                    letter_value = 1 if current_letter == 'S' else 2
                    board[position[1]][position[0]] = (letter_value, player)  # Updated to tuple format
                    drawCell(mySurface, board, position[1], position[0])
                    total_sos_count = handleSOS(mySurface, board, n, sos_scores, total_sos_count, processed_sos)
                    if isBoardFull(board):
                        winning_player = determineWinner(sos_scores)
                        if winning_player:
                            displayWinnerMessage(mySurface, winning_player)
                            pygame.display.update()
                            pygame.time.wait(2000)  # Show message for 2 seconds
                            inProgress = False
                printBoard(board,f)
                f.write('Scores: Blue - ' + str(sos_scores[0]) + ' Red - ' + str(sos_scores[1]) + '\n' + '\n')
                player = 2 if player == 1 else 1
                f.write('Current Player: ' + str(player) + '\n')

            elif event.type == KEYDOWN:
                if event.key == K_s:
                    current_letter = 'S'
                elif event.key == K_o:
                    current_letter = 'O'

            elif event.type == QUIT:
                inProgress = False


        displayScore(mySurface, n, sos_scores)
        displayPlayer(mySurface, n, player)
        pygame.display.update()

    pygame.quit()
