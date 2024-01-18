from sosGame import *
from sosAlgorithms import *
import random

def identifyPotentialMoves(board, n):
    potential_moves = []
    best_moves = []

    is_board_empty = all(cell is None for row in board for cell in row)

    for i in range(n):
        for j in range(n):
            if board[i][j] is None:  # Empty cell
                for letter in ['S', 'O']:
                    move = (i, j, letter)
                    if is_board_empty:
                        potential_moves.append(move)  # All moves are potential on an empty board
                    else:
                        if canFormSOS(board, n, i, j, letter):
                            best_moves.append(move)
                        elif setsUpFutureSOS(board, n, i, j, letter):
                            best_moves.append(move)
                        elif blocksOpponentSOS(board, n, i, j, letter):
                            best_moves.append(move)

    return best_moves if best_moves else potential_moves


def canFormSOS(board, n, i, j, letter):
    if letter not in ['S', 'O']:
        return False

    temp_board = [row[:] for row in board]
    letter_value = 1 if letter == 'S' else 2
    temp_board[i][j] = (letter_value, None)  # Assuming None for player as it's a hypothetical move

    # Function to check for SOS in a direction
    def checkDirection(cells):
        def is_valid_cell(cell, expected_value):
            return isinstance(cell, tuple) and cell[0] == expected_value

        return (is_valid_cell(cells[0], 1) and
                is_valid_cell(cells[1], letter_value) and
                is_valid_cell(cells[2], 1))

    # Check all directions for SOS
    directions = [
        [(i, j-1), (i, j), (i, j+1)],  # Horizontal
        [(i-1, j), (i, j), (i+1, j)],  # Vertical
        [(i-1, j-1), (i, j), (i+1, j+1)],  # Diagonal
        [(i-1, j+1), (i, j), (i+1, j-1)]  # Reverse Diagonal
    ]

    for direction in directions:
        cells = [temp_board[x][y] if 0 <= x < n and 0 <= y < n else None for x, y in direction]
        if checkDirection(cells):
            return True

    return False

def setsUpFutureSOS(board, n, i, j, letter):
    if letter not in ['S', 'O']:
        return False

    temp_board = [row[:] for row in board]
    letter_value = 1 if letter == 'S' else 2
    temp_board[i][j] = (letter_value, None)  # Assuming None for player as it's a hypothetical move

    # Function to check for setup in a direction
    def checkSetup(cells):
        def is_empty_or_letter(cell, expected_letter_value):
            return cell is None or (isinstance(cell, tuple) and cell[0] == expected_letter_value)

        if letter_value == 1:  # For letter 'S'
            return is_empty_or_letter(cells[0], 2) and is_empty_or_letter(cells[2], 2)
        else:  # For letter 'O'
            return ((isinstance(cells[0], tuple) and cells[0][0] == 1) and is_empty_or_letter(cells[2], 2)) or \
                   (is_empty_or_letter(cells[0], 2) and (isinstance(cells[2], tuple) and cells[2][0] == 1))

    # Check all directions for potential setup
    directions = [
        [(i, j-1), (i, j), (i, j+1)],  # Horizontal
        [(i-1, j), (i, j), (i+1, j)],  # Vertical
        [(i-1, j-1), (i, j), (i+1, j+1)],  # Diagonal
        [(i-1, j+1), (i, j), (i+1, j-1)]  # Reverse Diagonal
    ]

    for direction in directions:
        cells = [temp_board[x][y] if 0 <= x < n and 0 <= y < n else None for x, y in direction]
        if checkSetup(cells):
            return True

    return False




def blocksOpponentSOS(board, n, i, j, letter):
    if letter not in ['S', 'O']:
        return False

    temp_board = [row[:] for row in board]
    letter_value = 1 if letter == 'S' else 2
    temp_board[i][j] = (letter_value, None)  # Assuming None for player as it's a hypothetical move

    # Function to check if a sequence forms SOS for the opponent
    def isOpponentSOS(seq):
        opponent_letter_value = 2 if letter == 'S' else 1  # Opponent's letter value

        # Safe check for tuple values in the sequence
        def is_valid_tuple(cell, expected_letter_value):
            return isinstance(cell, tuple) and cell[0] == expected_letter_value

        # Check for opponent SOS in the sequence
        return any((is_valid_tuple(seq[k], opponent_letter_value) and seq[k+1] == (letter_value, None) and 
                    is_valid_tuple(seq[k+2], opponent_letter_value)) for k in range(1))

    # Check all directions for potential block
    directions = [
        [(i, j-1), (i, j), (i, j+1)],  # Horizontal
        [(i-1, j), (i, j), (i+1, j)],  # Vertical
        [(i-1, j-1), (i, j), (i+1, j+1)],  # Diagonal
        [(i-1, j+1), (i, j), (i+1, j-1)]  # Reverse Diagonal
    ]

    for direction in directions:
        cells = [temp_board[x][y] if 0 <= x < n and 0 <= y < n else None for x, y in direction]
        if isOpponentSOS(cells):
            return True

    return False



def evaluateMove(board, n, move, opponent):
    i, j, letter = move
    score = 0

    # Significantly increase score for creating SOS
    if canFormSOS(board, n, i, j, letter):
        score += 100

    # Moderate increase for setting up future SOS
    if setsUpFutureSOS(board, n, i, j, letter):
        score += 30

    # Slight increase for blocking opponent's SOS
    if blocksOpponentSOS(board, n, i, j, letter):
        score += 70

    return score



def selectBestMove(potential_moves, board, n, current_player_letter):
    best_score = -1
    best_move = None

    # Determine the opponent's letter
    opponent_letter = 'O' if current_player_letter == 'S' else 'S'

    for move in potential_moves:
        score = evaluateMove(board, n, move, opponent_letter)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def computerMove(board, n, current_player_letter):
    potential_moves = identifyPotentialMoves(board, n)

    if potential_moves:
        # Select the best move among all potential moves
        best_move = selectBestMove(potential_moves, board, n, current_player_letter)
        return best_move
    else:
        # If no strategic moves are available, find the first empty cell and randomly choose 'S' or 'O'
        empty_cells = [(i, j) for i in range(n) for j in range(n) if board[i][j] is None]
        if empty_cells:
            i, j = random.choice(empty_cells)
            letter = random.choice(['S', 'O'])
            return (i, j, letter)

    print("No moves available")
    return None
