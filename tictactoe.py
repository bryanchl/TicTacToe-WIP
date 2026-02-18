# STARTED ON 050126, arnd 1300
# TicTacToev1 Completed on 120126

import tkinter as tk
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
       
        self.resizable(False, False)
        self.title("TicTacToe - v2")
        self.iconbitmap("ttt-icon.ico")
        self.existing_game = False

        appsize_w = 1280
        appsize_h = 720
        launch_xpos = int((self.winfo_screenwidth() - appsize_w) / 2)
        launch_ypos = int((self.winfo_screenheight() - appsize_h) / 2)
        self.geometry(f"{appsize_w}x{appsize_h}+{launch_xpos}+{launch_ypos}")
        self.config(bg="light blue")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.menu_btns_frame = tk.Frame(master=self, borderwidth=2, bg="light blue")
        self.menu_btns_frame.grid(row=0, column=0)

        self.player_game_reset_btn = tk.Button(master=self.menu_btns_frame, text="Player vs Player", command=lambda: self.new_game(False), width=35, height=2, font=25, bg="grey", borderwidth=0)
        self.bot_game_back_btn = tk.Button(master=self.menu_btns_frame, text="Player vs Bot", command=lambda: self.new_game(True), width=35, height=2, font=25, bg="grey", borderwidth=0)
        self.exit_game = tk.Button(master=self.menu_btns_frame, text="Exit", command=self.destroy, width=35, height=2, font=25, bg="grey", borderwidth=0)
        self.player_game_reset_btn.grid(row=0, column=0, pady=10)
        self.bot_game_back_btn.grid(row=1, column=0, pady=10)
        self.exit_game.grid(row=2, column=0, pady=10)

### DECORATORS---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # def newGameDecorators(newGameFunc):
    #     def enhanced(self, *args, **kwargs):
    #         newGameFunc(self, *args, **kwargs)
    #         self.player_game_reset_btn.config(text="3x3", command=lambda: self.select_bot_difficulty(3))
    #         self.bot_game_back_btn.config(text="4x4", command=lambda: self.select_bot_difficulty(4))
    #         self.exit_game.config(text="5x5", command=lambda: self.select_bot_difficulty(5))
    #     return enhanced
    
### GAME START / STOP / CUSTOMIZE FUNCTIONS----------------------------------------------------------------------------------------------------------------------------------------------
    # @newGameDecorators
    def new_game(self, bot_game):
        self.bot_game_flag = bot_game
        self.player_game_reset_btn.config(text="3x3", command=lambda: self.select_bot_difficulty(3))
        self.bot_game_back_btn.config(text="4x4", command=lambda: self.select_bot_difficulty(4))
        self.exit_game.config(text="5x5", command=lambda: self.select_bot_difficulty(5))

    # @newGameDecorators
    # def bot_new_game(self):
    #     self.bot_game_flag = True

    def select_bot_difficulty(self, boardsize):
        if self.bot_game_flag:
            self.player_game_reset_btn.config(text="Easy", command=lambda: self.init_game(boardsize, "easy"))
            self.bot_game_back_btn.config(text="Standard", command=lambda: self.init_game(boardsize, "standard"))
            if boardsize == 3:
                self.exit_game.config(text="Impossible", command=lambda: self.init_game(boardsize, "impossible"))
            else:
                self.exit_game.grid_remove()
        else:
            self.init_game(boardsize, None)
    
    def back(self):
        self.player_game_reset_btn.config(text="Player vs Player", command=lambda: self.new_game(False))
        self.bot_game_back_btn.config(text="Player vs Bot", command=lambda: self.new_game(True))
        self.board.destroy()

    def win_end(self, winner):
        winnerText = f"Player {winner} won!"
        self.board.unbind("<1>")
        for sq in self.winSquares :
            self.board.itemconfig(sq, fill="light green")
            self.board.lower(sq)
        EndScreen(winnerText)
    
    def draw_end(self):
        winnerText = "It's a Tie!"
        self.board.unbind("<1>") 
        EndScreen(winnerText)

### GAME INITIALIZATION-----------------------------------------------------------------------------------------------------------------------------------------------------------------
    def init_game(self, size, bot_difficulty):
        self.boardsize = size
        self.bot_difficulty = bot_difficulty
        self.boardmatrix = [[0 for col in range(self.boardsize)] for row in range(self.boardsize)]
        self.winCheck = 0
        self.player_turn = 1
        self.bot_turn = 2
        self.occupied = []
        self.winSquares = []
        self.turn = 1 # 1 or 2 depending on player turn

        if self.existing_game:
            self.board.destroy()
        self.player_game_reset_btn.config(text="Reset", command=lambda: self.init_game(size, bot_difficulty))        
        self.bot_game_back_btn.config(text="Back To Menu", command=self.back)
        self.exit_game.config(text="Exit", command=self.destroy)
        self.exit_game.grid()
        
        self.create_board()
    
    def create_board(self):
        self.existing_game = True

        #board creation
        self.canvas_size = 600
        self.board = tk.Canvas(master=self, width=self.canvas_size, height=self.canvas_size, background="light grey", highlightthickness=0, borderwidth=0)
        self.board.grid(row=0, column=1, padx=(0,120))
        
        self.squareIDs = []
        for y in range(self.boardsize):
            consty = (self.canvas_size / self.boardsize) - (y // (self.boardsize - 1))  
            basey = y * self.canvas_size / self.boardsize
            for x in range(self.boardsize):
                constx = (self.canvas_size / self.boardsize) - (x // (self.boardsize - 1))
                basex = x * self.canvas_size / self.boardsize
                square = self.board.create_rectangle(basex,basey,basex+constx,basey+consty)
                self.squareIDs.append(square)

        self.board.bind("<1>",self.player_click)
        
    def player_click(self, event):
        self.boardcol = int(event.x // (self.canvas_size / self.boardsize))
        self.boardrow = int(event.y // (self.canvas_size / self.boardsize))
        self.make_move(self.boardcol, self.boardrow)
        
    def make_move(self, boardcol, boardrow):
        if [boardcol,boardrow] in self.occupied:
            return
        self.occupied.append([boardcol,boardrow])

        topX = (0.25 * self.canvas_size / self.boardsize) + boardcol * (self.canvas_size / self.boardsize)
        botX = (0.75 * self.canvas_size / self.boardsize) + boardcol * (self.canvas_size / self.boardsize)
        topY = (0.25 * self.canvas_size / self.boardsize) + boardrow * (self.canvas_size / self.boardsize)
        botY = (0.75 * self.canvas_size / self.boardsize) + boardrow * (self.canvas_size / self.boardsize)

        if self.turn == 1:
            self.boardmatrix[boardrow][boardcol] = 1
            self.board.create_line(topX,topY,botX,botY, width=2)
            self.board.create_line(topX,botY,botX,topY, width=2)
        elif self.turn == 2:
            self.boardmatrix[boardrow][boardcol] = 2
            self.board.create_oval(topX,topY,botX,botY, width=2)

        if len(self.occupied) >= 2 * self.boardsize - 1:
            print(self.boardmatrix)
            self.check_win()
            print(len(self.occupied))
        if len(self.occupied) == self.boardsize**2 and self.winCheck == 0:
            return self.draw_end()
        
        self.turn = 3 - self.turn
        if self.winCheck == 0 and self.bot_game_flag and self.turn == self.bot_turn:
            self.bot_move()
        
    def bot_move(self):
        if len(self.occupied) == 1:
            if self.boardsize % 2 == 1:
                midsq = (int((self.boardsize - 1) / 2),int((self.boardsize - 1) / 2))
                if [self.boardcol,self.boardrow] == [*midsq]:
                    randcol = random.randint(0,1) * (self.boardsize - 1)
                    randrow = random.randint(0,1) * (self.boardsize - 1)
                    self.make_move(randcol, randrow)
                else:
                    self.make_move(*midsq)
            else:
                midsq = int(self.boardsize / 2)
                randcol = random.randint(midsq-1,midsq)
                randrow = random.randint(midsq-1,midsq)
                if randcol == self.boardcol and randrow == self.boardrow:
                    randcol = self.boardsize - 1 - randcol
                    randrow = self.boardsize - 1 - randrow
                self.make_move(randcol, randrow)
        else:
            bot_countermove = self.bot_counter()
            self.boardcol = bot_countermove[0]
            self.boardrow = bot_countermove[1]
            self.make_move(*bot_countermove)

    def bot_counter(self):
        if self.bot_difficulty != "easy":
            winPossible = [self.diagWin(self.bot_turn), self.negDiagWin(self.bot_turn), self.horiWin(self.bot_turn), self.vertWin(self.bot_turn)]
            for possibilities in winPossible:
                if possibilities:
                    print("FINISH HIM")
                    return possibilities
                
        counterMoves = [self.horiWin(self.player_turn), self.vertWin(self.player_turn)]
        # counter diagonal wins
        if self.boardcol == self.boardrow:
            counterMoves.append(self.diagWin(self.player_turn))
        # counter neg diagonal wins
        if self.boardcol + self.boardrow == self.boardsize - 1:
            counterMoves.append(self.negDiagWin(self.player_turn))
        for possibilities in counterMoves:
            if possibilities:
                print("FULL COUNTER")
                return possibilities
            
        edgeNeeded = -1
        edgeSelected = -1
        while True:
            if len(self.occupied) == 3 and self.bot_difficulty == "impossible":
                if self.boardmatrix[1][1] == 1:
                    randcol = random.randint(0,1) * (self.boardsize - 1)
                    randrow = random.randint(0,1) * (self.boardsize - 1)
                else:
                    edgeNeeded = 1
                    randcol = random.randint(0,1) * (self.boardsize - 2)
                    randrow = random.randint(0,1) * (self.boardsize - 2)
                    if randcol == 1 or randrow == 1:
                        edgeSelected = 1
            else:
                randcol = random.randint(0,self.boardsize-1)
                randrow = random.randint(0,self.boardsize-1)
            if [randcol, randrow] not in self.occupied and edgeNeeded*edgeSelected == 1:
                break
            
        return randcol, randrow
    
    def diagWin(self, turn):
        count = 0
        diagPlayed = []
        for sq in range(self.boardsize):
            diagPlayed.append(self.boardmatrix[sq][sq])
            if self.boardmatrix[sq][sq] == turn:
                count += 1
        if count == self.boardsize-1 and sum(diagPlayed) == (self.boardsize-1) * turn:
            return (diagPlayed.index(0), diagPlayed.index(0))
        return None
        
    def negDiagWin(self, turn):
        count = 0
        negDiagPlayed = []
        for sq in range(self.boardsize):
            negDiagPlayed.append(self.boardmatrix[sq][self.boardsize - sq - 1])
            if self.boardmatrix[sq][self.boardsize - sq - 1] == turn:
                count += 1
        if count == self.boardsize-1 and sum(negDiagPlayed) == (self.boardsize-1) * turn:        
            return (self.boardsize - negDiagPlayed.index(0) - 1, negDiagPlayed.index(0))
        return None

    def horiWin(self, turn):
        for row in self.boardmatrix:
            count = 0
            for col in row:
                if col == turn:
                    count += 1
            if count == self.boardsize-1 and sum(row) == (self.boardsize-1) * turn:
                print(self.boardmatrix)
                return row.index(0), self.boardmatrix.index(row)
        return None
    
    def vertWin(self, turn):
        for col in range(len(self.boardmatrix)):
            count = 0
            colPlayed = []
            for row in range(len(self.boardmatrix[col])):
                colPlayed.append(self.boardmatrix[row][col])
                if self.boardmatrix[row][col] == turn:
                    count += 1
            if count == self.boardsize-1 and sum(colPlayed) == (self.boardsize-1) * turn:
                return col, colPlayed.index(0)
        return None
    
    def check_win(self):
        # diagonal win condition
        diagWinSquares = []
        if self.boardrow == self.boardcol:
            for size in range(self.boardsize):
                if self.boardmatrix[size][size] != self.turn:
                    diagWinSquares.clear()
                    break
                diagWinSquares.append(1 + (self.boardsize + 1) * size)

        if len(diagWinSquares) >= self.boardsize:
            self.winSquares += diagWinSquares
            self.board.create_line(self.canvas_size*0.1,self.canvas_size*0.1,self.canvas_size*0.9,self.canvas_size*0.9, fill="yellow", width=5)
            self.winCheck += 1
        
        # neg diagonal win condition
        negDiagWinSquares = []
        if self.boardrow + self.boardcol == self.boardsize - 1:
            for size in range(self.boardsize):
                if self.boardmatrix[size][self.boardsize - 1 - size] != self.turn:
                    negDiagWinSquares.clear()
                    break
                negDiagWinSquares.append(self.boardsize + (self.boardsize - 1) * size)

        if len(negDiagWinSquares) >= self.boardsize:
            self.winSquares += negDiagWinSquares
            self.board.create_line(self.canvas_size*0.1,self.canvas_size*0.9,self.canvas_size*0.9,self.canvas_size*0.1, fill="yellow", width=5)
            self.winCheck += 1

        # horizontal win condition
        horiWinSquares = []
        for col in range(len(self.boardmatrix[self.boardrow])):
            if self.boardmatrix[self.boardrow][col] != self.turn:
                horiWinSquares.clear()
                break    
            horiWinSquares.append(self.boardrow*self.boardsize + col + 1)
        
        if len(horiWinSquares) >= self.boardsize:
            self.winSquares += horiWinSquares
            rowCoord = (self.canvas_size*(self.boardrow + 0.5)) / self.boardsize
            self.board.create_line(self.canvas_size*0.1,rowCoord,self.canvas_size*0.9,rowCoord, fill="yellow", width=5)
            self.winCheck += 1

        # vertical win condition
        vertWinSquares = []
        for row in range(len(self.boardmatrix[self.boardcol])):
            if self.boardmatrix[row][self.boardcol] != self.turn:
                vertWinSquares.clear()
                break    
            vertWinSquares.append(row*self.boardsize + self.boardcol + 1)

        if len(vertWinSquares) >= self.boardsize:
            self.winSquares += vertWinSquares
            colCoord = (self.canvas_size*(self.boardcol + 0.5)) / self.boardsize
            self.board.create_line(colCoord,self.canvas_size*0.1,colCoord,self.canvas_size*0.9, fill="yellow", width=5)
            self.winCheck += 1

        if self.winCheck > 0:
            self.win_end(self.turn)

        if self.winCheck > 1:
            print("Easter Egg 1") # easter egg 1

class EndScreen(tk.Toplevel):
    def __init__(self, winnerText):
        super().__init__()

        appsize_w = 350
        appsize_h = 250
        launch_xpos = int((self.winfo_screenwidth() - appsize_w) / 2)
        launch_ypos = int((self.winfo_screenheight() - appsize_h) / 2)
        self.geometry(f"{appsize_w}x{appsize_h}+{launch_xpos}+{launch_ypos}")
        self.attributes("-topmost", True)
        self.config(bg="#C0C0C0")
        self.grab_set()
        self.overrideredirect(True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=6)
        self.grid_rowconfigure(1, weight=4)
        
        winnerLabel = tk.Label(master=self, text=f"{winnerText}", width=40, height=3, bg="#C0C0C0", font=("Helvetica", 14), anchor="s")
        reset = tk.Button(master=self, text="Play Again", command=self.reset, width=15, height=2, font=2, borderwidth=0, bg="grey")
        close = tk.Button(master=self, text="Close", command=self.destroy, width=15, height=2, font=2, borderwidth=0, bg="grey")
        winnerLabel.grid(row=0, column=0, columnspan=3)
        reset.grid(row=1, column=0, sticky="e")
        close.grid(row=1, column=2, sticky="w")

    def reset(self):
        self.destroy()
        print(game.bot_difficulty)
        game.init_game(game.boardsize,game.bot_difficulty)
        return

game = TicTacToe()
game.mainloop()