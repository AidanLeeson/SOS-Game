import pygame
import unittest
from sosGame import newBoard, possibleSquare, checkForSOS, determineWinner, countPlayerPiecesInLine, handleSOS, newBoard
from sosComp import computerMove, identifyPotentialMoves, evaluateMove, selectBestMove, canFormSOS, setsUpFutureSOS, blocksOpponentSOS  # Import your game functions here


class TestSOSGame(unittest.TestCase):

    def test_new_board(self):
        size = 5
        expected_board = [[None] * size for _ in range(size)]
        self.assertEqual(newBoard(size), expected_board, "Board initialization failed.")

    def test_possible_square(self):
        # Update the board to use tuples for non-empty cells and None for empty cells
        board = [[None, (1, 1)], [(2, 2), None]]  # Assuming (1, 1) represents 'S' and (2, 2) represents 'O'

        # Test for an available square
        self.assertTrue(possibleSquare(board, 2, 0, 0), "Square should be available.")

        # Test for a non-available square
        self.assertFalse(possibleSquare(board, 2, 0, 1), "Square should not be available.")

    def test_check_for_sos(self):
        board = [
            [(1, 1), (2, 2), (1, 1), None, None],
            [None, None, None, None, None],
            [None, None, (1, 3), (2, 3), (1, 3)],
            [None, None, None, None, None],
            [(1, 5), None, None, None, (1, 5)]
        ]
        n = 5
        processed_sos = []
        expected_lines = [(((0, 0), (0, 1), (0, 2)), 1), (((2, 2), (2, 3), (2, 4)), 3)]  # Adjusted to match output format
        self.assertEqual(checkForSOS(board, n, processed_sos), expected_lines, "SOS detection failed.")


    def test_determine_winner(self):
        scores = [3, 5]
        self.assertEqual(determineWinner(scores), 2, "Winner determination failed.")
        scores = [5, 5]
        self.assertIsNone(determineWinner(scores), "Draw determination failed.")

    def test_majority_player1(self):
        # Updated board with tuple format
        board = [
            [(1, 1), (2, 2), (1, 1)],
            [(2, 2), (1, 1), (2, 2)],
            [None, None, None]
        ]
        line = [(0, 0), (0, 1), (0, 2)]
        self.assertEqual(countPlayerPiecesInLine(line, board), 1, "Player 1 should have the majority")

    def test_majority_player2(self):
        # Updated board with tuple format
        board = [
            [(1, 1), (2, 2), (1, 1)],
            [(2, 2), (1, 1), (2, 2)],
            [None, None, None]
        ]
        line = [(1, 0), (1, 1), (1, 2)]
        self.assertEqual(countPlayerPiecesInLine(line, board), 2, "Player 2 should have the majority")

    def test_equal_pieces(self):
        # Updated board with tuple format
        board = [
            [(1, 1), (2, 2), (1, 1)],
            [(2, 2), (1, 1), (2, 2)],
            [None, None, None]
        ]
        # Adjust the line so it includes one piece from each player
        line = [(0, 0), (0, 1)]  # One piece from Player 1 at (0, 0) and one piece from Player 2 at (0, 1)
        self.assertEqual(countPlayerPiecesInLine(line, board), 0, "Players should have an equal number of pieces")

    def test_empty_line(self):
        # Updated board with tuple format
        board = [
            [(1, 1), (2, 2), (1, 1)],
            [(2, 2), (1, 1), (2, 2)],
            [None, None, None]
        ]
        line = [(2, 0), (2, 1), (2, 2)]
        self.assertEqual(countPlayerPiecesInLine(line, board), 0, "Line is empty, should return 0")

    def test_identifyPotentialMoves_emptyBoard(self):
        # Board already in the correct format (all cells are None)
        board = [[None] * 3 for _ in range(3)]
        n = 3
        expected_moves = [(i, j, letter) for i in range(n) for j in range(n) for letter in ['S', 'O']]
        self.assertEqual(identifyPotentialMoves(board, n), expected_moves)

    def test_identifyPotentialMoves_withMoves(self):
        # Updated board with tuple format
        board = [[(1, 1), None, None], [None, (2, 2), None], [None, None, None]]  # Assuming (1, 1) represents 'S' and (2, 2) represents 'O'
        n = 3
        potential_moves = identifyPotentialMoves(board, n)
        self.assertTrue((0, 1, 'O') in potential_moves)  # Check if this move is still valid

    def test_evaluateMove(self):
        # Updated board with tuple format
        board = [
            [(1, 1), None, None],
            [None, (2, 2), None],
            [None, None, None]
        ]
        n = 3

        # Example move to evaluate
        move = (0, 1, 'O')  # Placing 'O' at (0, 1)
        opponent = 'S'  # Assuming 'S' is the opponent's letter

        # Convert 'S' and 'O' to their respective numeric representations (1 for 'S', 2 for 'O')
        letter_value = 1 if move[2] == 'S' else 2

        # Update the board temporarily to simulate the move
        temp_board = [row[:] for row in board]
        temp_board[move[0]][move[1]] = (letter_value, 3)  # Assuming player 3 is making the move for test purposes

        # Evaluate the move
        evaluated_score = evaluateMove(temp_board, n, move, opponent)

        # Define expected score based on game logic
        expected_score = 0
        if canFormSOS(temp_board, n, move[0], move[1], move[2]):
            expected_score += 100
        if setsUpFutureSOS(temp_board, n, move[0], move[1], move[2]):
            expected_score += 30
        if blocksOpponentSOS(temp_board, n, move[0], move[1], move[2]):
            expected_score += 70

        # Assert that the evaluated score matches the expected score
        self.assertEqual(evaluated_score, expected_score, "Move evaluation score is incorrect")

            
    # Check if the best move selection is consistent with the scoring logic
    def test_selectBestMove(self):
        board = [[1, 0, 0], [0, 2, 0], [0, 0, 0]]
        n = 3
        potential_moves = [(0, 1, 'O'), (1, 1, 'S')]
        current_player_letter = 'O'  # Set the current player's letter
        best_move = selectBestMove(potential_moves, board, n, current_player_letter)
        self.assertEqual(best_move, (0, 1, 'O'))

    # Ensure the computer can make a valid move
    def test_computerMove(self):
        # Updated board with tuple format
        board = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, (1, 1), (2, 2), None],  # 'S' placed by player 1 and 'O' placed by player 2
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]
        n = 5
        current_player_letter = 'O'  # Make sure this variable is defined
        move = computerMove(board, n, current_player_letter)
        self.assertIsNotNone(move, "Computer move should not be None")

    def test_handle_sos(self):
        # Initialize a test board
        n = 3
        board = newBoard(n)
        board[0][0] = (1, 1)  # 'S' by Player 1
        board[0][1] = (2, 2)  # 'O' by Player 2
        board[0][2] = (1, 1)  # 'S' by Player 1
        sos_scores = [0, 0]
        total_sos_count = 0
        processed_sos = []

        # Call handleSOS
        total_sos_count = handleSOS(None, board, n, sos_scores, total_sos_count, processed_sos)

        # Check if the SOS was detected and scored correctly
        self.assertEqual(sos_scores, [1, 0], "SOS scoring failed")
        self.assertEqual(total_sos_count, 1, "SOS count is incorrect")


if __name__ == '__main__':
    unittest.main()
