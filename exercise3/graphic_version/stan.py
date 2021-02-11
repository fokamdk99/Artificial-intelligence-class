import copy

class State():
    board = None
    terminal = None
    winner = None
    value = None
    max_player = None #if player's turn, True; else False
        
    def __init__(self, max_player, board=None):
        if board == None:
            self.board = [["-","-","-"],["-","-","-"],["-","-","-"]]
        else:
            self.board = board

        self.max_player = max_player
        self.check_if_terminal() 


    def __lt__(self, o):
        if (self.value < o.value):
            return True
        else:
            return False

    def __gt__(self, o):
        if (self.value > o.value):
            return True
        else:
            return False

    #check if current state is terminal
    def check_if_terminal(self):
        self.terminal = False
        for i in range(0,3):
            player_type = self.board[i][0]
            if (self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2] and player_type != "-"):
                self.terminal = True
                self.winner = player_type
                return

        for i in range(0,3):
            player_type = self.board[0][i]
            if (self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and player_type != "-"):
                self.terminal = True
                self.winner = player_type
                return

        player_type = self.board[1][1]
        if (self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and player_type != "-"):
            self.terminal = True
            self.winner = player_type
            return

        if (self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and player_type != "-"):
            self.terminal = True
            self.winner = player_type
            return

        licznik = 0
        for row in range(0,3):
            for column in range(0,3):
                if self.board[row][column] == "-":
                    licznik += 1

        if licznik == 0:
            self.terminal = True
            self.winner = "-"

    #return payoff value
    def get_payoff(self):
        if self.winner == "p":
            return 100
        elif self.winner == "o":
            return -100
        elif self.winner == "-":
            return 0

    #return heuristics value
    def get_heuristic(self):
        heuristic_table = [[3,2,3],[2,4,2],[3,2,3]]
        player = 0
        opponent = 0
        for row in range(0,3):
            for column in range(0,3):
                if self.board[row][column] == "p":
                    player += heuristic_table[row][column]
                if self.board[row][column] == "o":
                    opponent += heuristic_table[row][column]
        
        if self.max_player:
            return (player - opponent)
        else:
            return -(player - opponent)
                

    #determine value of the current state
    def get_state_value(self):
        if self.terminal:
            self.value = self.get_payoff()
        else:
            self.value = self.get_heuristic()

    #return list of successors
    def get_successors(self):
        successors = []
        if self.max_player:
            player_type = "o"
        else:
            player_type = "p"
        for row in range(0,3):
            for column in range(0,3):
                if self.board[row][column] == "-":
                    #licznik += 1
                    self.board[row][column] = player_type
                    tmp_board = copy.deepcopy(self.board)
                    #print(f"tmp_board:\n{tmp_board}")
                    successor = State(not self.max_player, tmp_board)
                    successors.append(successor)
                    
                    self.board[row][column] = "-"

        return successors

    def show_board(self):
        for row in range(0,3):
            for column in range(0,3):
                print(f"{self.board[row][column]}, ", end='')
            print("\n")
        print("\n\n")
        
    #save player's movement
    def make_move(self, row, column):
        if self.max_player:
            self.board[row][column] = "p"
        else:
            self.board[row][column] = "o"
        new_state = State(self.max_player, copy.deepcopy(self.board))
        return new_state