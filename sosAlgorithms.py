def newBoard(n):
    return [[None for _ in range(n)] for _ in range(n)]

def possibleSquare(board, n, i, j):
    return board[i][j] is None

def isButtonClicked(x, y, width, height, mousePos):
    mouseX, mouseY = mousePos
    return (x <= mouseX <= x + width) and (y <= mouseY <= y + height)

def checkForSOS(board, n, processed_sos):
    print("Current Board:")
    for row in board:
        print(" ".join(str(cell) if cell is not None else 'None' for cell in row))

    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # right, down, diagonal down-right, diagonal up-right
    new_sos_lines = []

    for i in range(n):
        for j in range(n):
            if board[i][j] is not None and board[i][j][0] == 1:  # Check for 'S' represented by (1, _)
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if 0 <= x < n and 0 <= y < n and board[x][y] is not None and board[x][y][0] == 2:  # Check for 'O'
                        x2, y2 = x + dx, y + dy
                        if 0 <= x2 < n and 0 <= y2 < n and board[x2][y2] is not None and board[x2][y2][0] == 1:  # Check for 'S'
                            sos_line = (((i, j), (x, y), (x2, y2)), board[x2][y2][1])  # Get the player who completed the SOS
                            if sos_line not in processed_sos:
                                print(f"Found 'SOS' at ({i}, {j}), ({x}, {y}), ({x2}, {y2}) by player {sos_line[1]}")
                                new_sos_lines.append(sos_line)
                                processed_sos.append(sos_line)

    return new_sos_lines













