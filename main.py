import tkinter as tk
from tkinter import messagebox
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        pass

class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False
    def num_empty_squares(self):
        return self.board.count(' ')

class GUI:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.frame = tk.Frame(self.app)
        self.frame.pack()
        self.start_menu()

    def start_menu(self):
        self.start_button = tk.Button(self.frame, text="Start", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        self.start_button.destroy()
        self.game = TicTacToe()
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.frame, text=" ", font=('Helvetica', '20'), width=5, height=2, command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def on_click(self, i, j):
        if not self.game.current_winner:
            self.game.make_move(i * 3 + j, 'X')
            self.buttons[i][j]['text'] = 'X'
            self.buttons[i][j]['state'] = 'disabled'
            if self.game.current_winner:
                messagebox.showinfo("Game Over", "You won!")
                self.reset_game()
            elif self.game.empty_squares():
                move = SmartComputerPlayer('O').get_move(self.game)
                self.game.make_move(move, 'O')
                self.buttons[move // 3][move % 3]['text'] = 'O'
                self.buttons[move // 3][move % 3]['state'] = 'disabled'
                if self.game.current_winner:
                    messagebox.showinfo("Game Over", "Computer won!")
                    self.reset_game()
                elif not self.game.empty_squares():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.reset_game()

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].destroy()
        self.start_menu()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
