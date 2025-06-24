from mancala import Game, Board

border = "-"*48
#stole this little jawn off chatgpt
letters = {
        'A': [
            "  #  ",
            " # # ",
            "#####",
            "#   #"
        ],
        'C': [
            " ####",
            "#    ",
            "#    ",
            " ####"
        ],
        'L': [
            "#    ",
            "#    ",
            "#    ",
            "#####"
        ],
        'M': [
            "#   #",
            "## ##",
            "# # #",
            "#   #"
        ],
        'N': [
            "#   #",
            "##  #",
            "# # #",
            "#  ##"
        ]
    }
def print_mancala():
    text = "MANCALA"
    rows = [""] * 4

    for char in text:
        for i in range(4):
            rows[i] += letters[char][i] + "  "

    for row in rows:
        print(row)
    print(border)

def printBoard(game: Game, player_num: int):
    board = game.getBoard()
    other_player_num = 2 if player_num == 1 else 1
    current_player, other_player = (board.player1, board.player2) if player_num == 1 else (board.player1, board.player2)
    if player_num == 1:
        current_player = board.player1
        other_player = board.player2
    elif player_num == 2:
        current_player = board.player2
        other_player = board.player1
    else:
        raise Exception(f"player_num parameter must be 1 or 2, input was {player_num}")
    
    #will slightly break when any pit gets >9 gems. should fix eventually
    print(f'\tP{other_player_num}: \t{other_player.get_pits()[::-1]}')
    print(f'\t     {other_player.get_store()}\t\t\t    {current_player.get_store()}')
    print(f'\tP{player_num}: \t{current_player.get_pits()}')

def getMove(player: int) -> int:
    message = f"Player {player}, make your move (enter 1-6): "
    move = int(input(message)) - 1
    return move

# long term: modify so that user selects human or ai for each player before game starts
if __name__ == '__main__':
    print()
    print_mancala()
    print()
    g = Game()
    current_player = 1
    #loop until game has ended
    while current_player != 0:
        printBoard(g, current_player)
        #ask for their move
        print()
        move = getMove(current_player)
        next_player = g.make_move(move)
        #loop until valid move is made
        while next_player == -1:
            print("Invalid move, try again.\n")
            move = getMove(current_player)
            next_player = g.make_move(move)
        if current_player == next_player:
            print("Ended move in store, play again.")
        else:
            print(f"\n{border}")
        current_player = next_player
        print()
        
    print("One player's pits are empty. The game is finished.")
    p1_store = g.board.player1.get_store()
    p2_store = g.board.player2.get_store()
    if p1_store > p2_store:
        print("Player 1 is the winner!")
    elif p2_store > p1_store:
        print("Player 2 is the winner!")
    else:
        print("Draw!")