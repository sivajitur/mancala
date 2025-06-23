gameStatus = False
class Player:
    def __init__(self, num, pits, store):
        self.pits = pits
        self.store = store
        self.num = num
    def get_pits(self):
        return self.pits
    def get_store(self):
        return(self.store)
    def set_pits(self, p):
        self.pits = p
    def set_store(self, s):
        self.store = s

class Board:
    def __init__(self):
        self.player1 = Player(1, pits = [4] * 6, store = 0)
        self.player2 = Player(2, pits = [4] * 6, store = 0)
    def get_player(self, player_num):
        if player_num == 1:
            return self.player1
        elif player_num == 2:
            return self.player2
        else:
            raise ValueError("Either 1 or 2")

    def print_board(self, player_num: int):
        other_player_num = 2 if player_num == 1 else 1
        if player_num == 1:
            current_player = self.player1
            other_player = self.player2
        elif player_num == 2:
            current_player = self.player2
            other_player = self.player1
        else:
            raise Exception(f"player parameter must be 1 or 2, input was {player_num}")
        print(f'P{other_player_num}: \t', other_player.get_pits()[::-1], '\t')
        print('     ', other_player.get_store(), '\t\t    ', current_player.get_store())
        print(f'P{player_num}: \t', current_player.get_pits(), '\t')
        
    def is_valid_move(self, pos, pits):
        if pos < 0 or pos > 5:
            return False
        return pits[pos] != 0
    
#Game class should only handle logic, not UI (user prompts). need to move UI to another class. makes it easier to tie in with training algorithm
class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 1 # 1 if Player 1, 2 if Player 2
   
    def is_game_over(self):
        return all(pit == 0 for pit in self.board.player1.get_pits()) or all(pit == 0 for pit in self.board.player2.get_pits()) 
    
    # move needs to take in a choice for a move and then output the board state and the next player
    def move(self):
        player_nums = [1,2] if self.current_player == 1 else [2,1]
        player_info = [(self.board.get_player(num), num) for num in player_nums]
        curr_player, curr_player_num = player_info[0]
        other_player, other_player_num = player_info[1]
        
        arr = curr_player.get_pits() + [curr_player.get_store()] + other_player.get_pits()
        print(arr)
        
        validMove = False
        while validMove is False:
            self.board.print_board(curr_player_num)
            arr_pos = int(input('Player ' + str(self.current_player) + ": Make your move (enter 1-6). Your pits: " + str(self.board.get_player(self.current_player).get_pits())+ '\n')) - 1
            validMove = self.board.is_valid_move(arr_pos, self.board.get_player(self.current_player).get_pits())
            if validMove is False:
                print('Invalid move! Try again bozo')
           
        print('Valid move')
 
        #save curr_pos%13 as a variable in the loop for consistency
        curr_pos = arr_pos
        num_stones = arr[arr_pos]
        arr[arr_pos] = 0
        for _ in range(num_stones):
            curr_pos = curr_pos + 1
            arr[curr_pos%13] = arr[curr_pos%13] + 1
            print(arr)
        if arr[curr_pos%13] == 1 and (curr_pos%13) in [0,1,2,3,4,5]:
            print("Capture!")
            arr[6] += arr[curr_pos%13] + arr[12 - (curr_pos%13)]
            arr[12 - (curr_pos%13)] = 0
            arr[curr_pos%13] = 0

        curr_player.set_pits(arr[0:6])
        curr_player.set_store(arr[6])
        other_player.set_pits(arr[7:13])

        if self.is_game_over():
            print("One player's pits are empty. The game is finished.")
            global gameStatus
            gameStatus = True
            p1_remaining_stones = sum(self.board.player1.get_pits())
            self.board.player1.set_store(self.board.player1.get_store() + p1_remaining_stones)
            p2_remaining_stones = sum(self.board.player2.get_pits())
            self.board.player2.set_store(self.board.player2.get_store() + p2_remaining_stones)
            return 

        #need to modify so that move returns state and next player instead of triggering next move
        if curr_pos == 6:
            print("You move again")
            self.move()
        else:
            print("End turn")
            self.board.print_board(self.current_player)
            if self.current_player == 1:
                self.current_player = 2
            else: 
                self.current_player = 1
        
      
def ideal_move(arr):
    pass
def ai_move(arr):
    resp = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': 'You are an expert in Mancala (Khala version capture). I will feed you an array. The first 6 values are your pits, the 7th value is your store. The last 6 values are your opponents pits. You want to maximize your store with minimizing your opponents. Follow the rules of Khala'},
        {'role': 'system', 'content': '''Kalah is played by two players on a board with two rows of 6 holes facing each other and two "kalahs" (the rightmost hole of each player).
        The stones are called "beans". At the beginning of the game, there are 6 beans in every hole. The kalahs are empty.	Start position

        The object of Kalah is to get as many beans into your own kalah by distributing them.
        A player moves by taking all the beans in one of his 6 holes and distributing them counterclockwise, by putting one bean in every hole including his, but excluding the opponent's kalah.

        There are two special moves:

        Extra move:
        If the last bean is distributed into his own kalah, the player may move again. He has to move again even if he does not want to.
        before the extra move	after the extra move
        Capture:
        If the last bean falls into an empty hole of the player and the opponent's hole above (or below) is not empty, the player puts his last bean and all the beans in his opponent's hole into his kalah.
        He has won all those beans.
        before the capture	after the capture
        The game ends if all 6 holes of one player become empty (no matter if it is this player's move or not).
        The beans in the other player's holes are given into this player's kalah.'''},
        {'role': 'user', 'content': f'{arr} What is the best move to make?'}
    ])
    print(resp['message']['content'])
           


if __name__ == '__main__':
    g = Game()

    while gameStatus is False:
        g.move()
    p1_store = g.board.player1.get_store()
    p2_store = g.board.player2.get_store()
    if p1_store > p2_store:
        print("Player 1 is the winner!")
    elif p2_store > p1_store:
        print("Player 2 is the winner!")
    else:
        print("Draw!")

        
