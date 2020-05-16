import math

# X is computer, O is human player
players = ['X', 'O']

def play_move(state, player, input_place):
    """Let player place their mark on the board"""
    while True:
        try:
            row, column = input_place.split(" ")
            break
        except ValueError:
            input_place = input("Please enter valid inputs (e.g 1 3, 2 2): ")

    if state[int(row)][int(column)] == " ":
        state[int(row)][int(column)] = player
    else:
        input_place = input("The position has already been occupied! Choose again: ")
        play_move(state, player, input_place)

def empty_cells(state):
    """"""
    cells = []
    for r, cell_row in enumerate(state):
        for c, cell in enumerate(cell_row):
            if cell == " ":
                cells.append([r, c])

    return cells

def evaluate(state, winner):
    """Return 1 if computer wins; -1 if human wins; 0 if draw"""
    if state == "Done" and winner == "X":
        return 1
    elif state == "Done" and winner == "O":
        return -1
    elif state == "Draw":
        return 0


def minimax(state, player, alpha=-math.inf, beta=math.inf):
    """"""
    winner, current_state = check_current_state(state)
    if current_state == "Draw" or current_state == "Done":
        return {"score": evaluate(current_state, winner), "move": "-1 -1"}

    best = {}

    if player == 'X':
        best["score"] = -math.inf
        best['move'] = ""
    else:
        best["score"] = math.inf
        best['move'] = ""

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        if player == "O":
            result = minimax(state, "X", alpha, beta)
        else:
            result = minimax(state, "O", alpha, beta)
        state[x][y] = " "
        result['move'] = "{} {}".format(x, y)

        # if player is computer
        if player == 'X':
            if result['score'] > best['score']:
                best = result
                alpha = max(best['score'], alpha)
        # if player is human
        else:
            if result['score'] < best['score']:
                best = result
                beta = min(best['score'], beta)

        if alpha >= beta:
            break

    return best


def display_board(state):
    """"""
    print("        0     1     2  ")
    print("     -------------------")
    print("  0  |  {}  |  {}  |  {}  |".format(state[0][0], state[0][1], state[0][2]))
    print("     ------+-----+------")
    print("  1  |  {}  |  {}  |  {}  |".format(state[1][0], state[1][1], state[1][2]))
    print("     ------+-----+------")
    print("  2  |  {}  |  {}  |  {}  |".format(state[2][0], state[2][1], state[2][2]))
    print("     -------------------")


def check_current_state(state):
    """"""
    win_state = [[state[0][0], state[0][1], state[0][2]],
                 [state[0][0], state[1][0], state[2][0]],
                 [state[1][0], state[1][1], state[1][2]],
                 [state[2][0], state[2][1], state[2][2]],
                 [state[0][1], state[1][1], state[2][1]],
                 [state[0][2], state[1][2], state[2][2]],
                 [state[0][0], state[1][1], state[2][2]],
                 [state[0][2], state[1][1], state[2][0]]]

    if ["X", "X", "X"] in win_state:
        return "X", "Done"
    elif ["O", "O", "O"] in win_state:
        return "O", "Done"
    elif len(empty_cells(state)) == 0:
        return None, "Draw"
    else:
        return None, "Not done"


if __name__ == "__main__":
    playing = True

    while playing:
        print("TIC TAC TOE")
        print("========================================")
        game_state = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        state = "Not done"
        display_board(game_state)
        while True:
            player = input("Please select player to go first (O is you, X is computer): ").upper()
            if player in players:
                if player == "X":
                    player_index = 0
                else:
                    player_index = 1
                break
            else:
                print("Please enter a valid input.")

        while state == "Not done":
            if player == "O":
                player_input = input("It's your turn. Please choose a position by entering 2 numbers seperated by a space to place your mark (e.g. row column - 2 1): ")
                play_move(game_state, player, player_input)

            else:
                print("It's computer's turn.")
                position = minimax(game_state, player)
                play_move(game_state, player, position['move'])
                print("The computer placed their mark on {}.".format(position['move']))

            display_board(game_state)
            print("- - - - - - - - - - - - - - - - - - - -")

            winner, state = check_current_state(game_state)

            if winner is not None:
                if winner == "X":
                    print("Computer won!")
                else:
                    print("You won!")
            else:
                player_index = (player_index + 1) % 2
                player = players[player_index]

            if state == "Draw":
                print("Draw!")


        print("-----------------------------------------")
        restart = input("Do you want to play again? Y/N: ").upper()
        if restart == "N":
            playing = False
