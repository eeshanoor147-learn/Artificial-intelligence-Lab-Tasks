import math
def minimax(current_Depth, node_Index, max_Turn, scores, target_Depth):
    # Base case: target depth reached
    if current_Depth == target_Depth:
        return scores[node_Index]
    # Maximizer's turn
    if max_Turn:
        return max(
            minimax(current_Depth + 1, node_Index * 2, False, scores, target_Depth),
            minimax(current_Depth + 1, node_Index * 2 + 1, False, scores, target_Depth)
        )
    # Minimizer's turn
    else:
        return min(
            minimax(current_Depth + 1, node_Index * 2, True, scores, target_Depth),
            minimax(current_Depth + 1, node_Index * 2 + 1, True, scores, target_Depth)
        )
# Driver code
scores = [3, 5, 2, 9, 3, 5, 2, 9]
# Tree depth
tree_Depth = int(math.log2(len(scores)))
print("The optimal value is:", minimax(0, 0, True, scores, tree_Depth))




import math
# Empty board
game = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
# Display board
def print_board():
    for r in game:
        print(r[0], "|", r[1], "|", r[2])
        print("---------")
#  for Check winner
def winner():
    #  for Rows
    for r in range(3):
        if game[r][0] == game[r][1] == game[r][2] and game[r][0] != ' ':
            return game[r][0]
    # for Columns
    for c in range(3):
        if game[0][c] == game[1][c] == game[2][c] and game[0][c] != ' ':
            return game[0][c]
    if game[0][0] == game[1][1] == game[2][2] and game[0][0] != ' ':
        return game[0][0]
    if game[0][2] == game[1][1] == game[2][0] and game[0][2] != ' ':
        return game[0][2]
    return None
def board_full():
    for r in game:
        if ' ' in r:
            return False
    return True
def minimax(isComputer):
    result = winner()
    if result == 'O':
        return 10
    if result == 'X':
        return -10
    if board_full():
        return 0
    # Computer move
    if isComputer:
        bestScore = -100
        for i in range(3):
            for j in range(3):
                if game[i][j] == ' ':
                    game[i][j] = 'O'
                    score = minimax(False)
                    game[i][j] = ' '
                    if score > bestScore:
                        bestScore = score
        return bestScore
    # Player move
    else:
        bestScore = 100
        for i in range(3):
            for j in range(3):
                if game[i][j] == ' ':
                    game[i][j] = 'X'
                    score = minimax(True)
                    game[i][j] = ' '
                    if score < bestScore:
                        bestScore = score
        return bestScore
def computer_turn():
    bestScore = -100
    moveRow = -1
    moveCol = -1
    for i in range(3):
        for j in range(3):
            if game[i][j] == ' ':
                game[i][j] = 'O'
                score = minimax(False)
                game[i][j] = ' '
                if score > bestScore:
                    bestScore = score
                    moveRow = i
                    moveCol = j
    game[moveRow][moveCol] = 'O'
while True:
    print_board()
    r = int(input("Enter row: "))
    c = int(input("Enter column: "))
    if game[r][c] != ' ':
        print("Already filled")
        continue
    game[r][c] = 'X'
    # Check player win
    if winner() == 'X':
        print_board()
        print("Player wins")
        break
    if board_full():
        print_board()
        print("Match draw")
        break
    # Computer move
    computer_turn()
    # Check computer win
    if winner() == 'O':
        print_board()
        print("Computer wins")
        break
    if board_full():
        print_board()
        print("Match draw")
        break