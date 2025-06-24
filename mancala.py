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
        
    def is_valid_move(self, pos, pits):
        if pos < 0 or pos > 5:
            return False
        return pits[pos] != 0
    
#Game class should only handle logic, not UI (user prompts). need to move UI to another class. makes it easier to tie in with training algorithm
class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 1 # 1 if Player 1, 2 if Player 2

    def getBoard(self) -> Board:
        return self.board
   
    def is_game_over(self) -> bool:
        return all(pit == 0 for pit in self.board.player1.get_pits()) or all(pit == 0 for pit in self.board.player2.get_pits()) 
    
    # move() takes in a move choice (int 1-6) and assumes that it comes from the correct player
    # it returns an int which says who the next player will be:
    #   1 for player 1
    #   2 for player 2
    #   0 if the game is finished
    #   -1 for an invalid move
    # we might eventually want to turn this into a tuple where the first number is this int
    # and the other elements give some other game info (ex. a capture occurred) so that it can be shown in a UI
    def make_move(self, move) -> int:
        #get objects for current and other player to avoid retreiving them later
        player_nums = [1,2] if self.current_player == 1 else [2,1]
        player_info = [(self.board.get_player(num), num) for num in player_nums]
        curr_player, curr_player_num = player_info[0]
        other_player, other_player_num = player_info[1]

        #check if move is valid
        if not self.board.is_valid_move(move, curr_player.get_pits()):
            return -1
        
        #create gem array
        arr = curr_player.get_pits() + [curr_player.get_store()] + other_player.get_pits()
        # add to debug
        #print(arr)
        
        #remove gems from selected pit and add them to 
        curr_pos = move
        num_gems = arr[curr_pos]
        arr[curr_pos] = 0
        for _ in range(num_gems):
            curr_pos = curr_pos + 1
            looped_pos = curr_pos%13
            arr[looped_pos] = arr[looped_pos] + 1

        #if move ends in an empty pit, capture all gems from that pit and the opposing pit
        if arr[looped_pos] == 1 and (looped_pos) in [0,1,2,3,4,5]:
            arr[6] += arr[looped_pos] + arr[12 - (looped_pos)]
            arr[12 - (looped_pos)] = 0
            arr[looped_pos] = 0

        #update board state with result of move
        curr_player.set_pits(arr[0:6])
        curr_player.set_store(arr[6])
        other_player.set_pits(arr[7:13])

        #if all of the pits on either side are empty, give the opponent all their remaining gems and then end the game
        if self.is_game_over():
            for player in [self.board.get_player(1), self.board.get_player(2)]:
                remaining_stones = sum(player.get_pits())
                player.set_store(player.get_store() + remaining_stones)
            return 0
        
        #if player didn't end in their own store, swap current player to the other player
        if looped_pos != 6:
            self.current_player = other_player_num
        
        #return number of player who makes the next move
        return self.current_player