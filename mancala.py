import ollama
class Player:
    def __init__(self, num, pits, store):
        self.pits = pits
        self.store = store
        self.num = num
    def get_pits(self):
        if self.num == 1:
            return(self.pits)
        else:
            return (self.pits[::-1])
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
            ValueError("Either 1 or 2")
    def print_board(self, flip = False):
        if flip:
            print('P1: \t', self.player1.get_pits()[::-1], '\t')
            print('     ', self.player1.get_store(), '\t\t    ', self.player2.get_store())
            print('P2: \t', self.player2.get_pits()[::-1], '\t')
        else:
            print('P2: \t', self.player2.get_pits(), '\t')
            print('     ', self.player2.get_store(), '\t\t    ', self.player1.get_store())
            print('P1: \t', self.player1.get_pits(), '\t')
    def is_valid_move(self, pos, pits):
        if pos < 0 or pos > 5:
            raise ValueError('Pass 1 to 6')
        return pits[pos] != 0
class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 1 # 1 if Player 1, 2 if Player 2
   
    def is_game_over(self):
        return all(pit == 0 for pit in self.board.player1.get_pits()) or all(pit == 0 for pit in self.board.player2.get_pits()) 
    
    
    def move(self):
        if self.current_player == 1:
            arr = self.board.get_player(1).get_pits() + [self.board.get_player(1).get_store()] + self.board.get_player(2).get_pits()[::-1]
        else:
            arr = self.board.get_player(2).get_pits()[::-1] + [self.board.get_player(2).get_store()] + self.board.get_player(1).get_pits()[::-1]
        print(arr)
        
        validMove = False
        while validMove is False:
            curr_player = self.current_player
            if curr_player == 2:
                self.board.print_board(flip = True)
            else:
                self.board.print_board()
            arr_pos = int(input('Player ' + str(self.current_player) + ": Make your move (enter 1-6). Your pits: " + str(self.board.get_player(self.current_player).get_pits())+ '\n')) - 1
            if arr_pos == 6:
                print("Hmm. So you want to learn what the ideal move is... mathematically\n")
                ideal_move(arr)
            elif arr_pos == -1:
                print("Hmm. So you want AI to give you the ideal move.\n")
                ai_move(arr)
            else:
                validMove = self.board.is_valid_move(arr_pos, self.board.get_player(self.current_player).get_pits())
           
        print('Valid move')
 
        curr_pos = arr_pos
        while arr[arr_pos] != 0:
            curr_pos = curr_pos + 1
            arr[curr_pos] = arr[curr_pos] + 1
            arr[arr_pos] = arr[arr_pos] - 1
            print(arr)
        if arr[curr_pos] == 1 and curr_pos != 6 and curr_pos in [0,1,2,3,4,5]:
            print("Capture!")
            arr[curr_pos] = arr[curr_pos] + arr[12 - curr_pos]
            arr[12 - curr_pos] = 0

        
        if self.current_player == 1:
            self.board.player1.set_pits(arr[0:6])
            self.board.player1.set_store(arr[6])
            self.board.player2.set_pits(arr[7:13])
        else:
            self.board.player2.set_pits(arr[0:6])
            self.board.player2.set_store(arr[6])
            self.board.player1.set_pits(arr[7:13])

    
        if curr_pos == 6:
            print("You move again")
            self.move()
        else:
            print("End turn")
            self.board.print_board()
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
    gameStatus = False
    while gameStatus is False:
        g.move()
        gameStatus = g.is_game_over()
        
