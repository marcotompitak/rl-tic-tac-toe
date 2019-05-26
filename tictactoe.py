from random import choice, random, shuffle
from collections import defaultdict


class TTTEnv:
    """
    Environment that encodes the rules of Tic Tac Toe, for the
    AI agents to interact with.
    """

    chars = ' XO'

    def __init__(self, playerX, playerO, visual=False):
        self.chars = type(self).chars
        self.playerX = playerX
        self.playerO = playerO
        self.visual = visual
        self.winning_lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                              (0, 3, 6), (1, 4, 7), (2, 5, 8),
                              (0, 4, 8), (2, 4, 6)]
        self.reset_board()

    def reset_board(self):
        self.board = [' '] * 9
        self.turn_parity = choice([1, -1])

    def is_valid(self, move: int):
        return self.board[move] == ' '

    def is_won(self):
        return any(not self.board[line[0]] == type(self).chars[0] and
                   self.board[line[0]] == self.board[line[1]
                                                     ] == self.board[line[2]]
                   for line in self.winning_lines)

    def is_stalemate(self):
        return not any(x == self.chars[0] for x in self.board)

    def play_game(self):
        self.playerX.reset()
        self.playerO.reset()
        self.reset_board()

        if self.visual:
            self.print_board()

        # Play game, maximum number of moves is 9
        for _ in range(9):
            player, opponent = (self.playerX, self.playerO)[::self.turn_parity]
            selected_move = player.choose_move(self.board)
            if not self.is_valid(selected_move):
                raise ValueError
            else:
                self.board[selected_move] = self.chars[self.turn_parity]
            if self.visual:
                print('\n')
                print(self.chars[self.turn_parity] +
                      ' goes for ' + str(selected_move + 1))
                self.print_board()
            if self.is_won():
                player.reward(100, self.board)
                player.notify_game_over()
                opponent.reward(-100, self.board)
                opponent.notify_game_over()
                if self.visual:
                    print('\n')
                    print(self.chars[self.turn_parity] + ' wins!')
                break
            elif self.is_stalemate():
                player.reward(50, self.board)
                player.notify_game_over()
                opponent.reward(50, self.board)
                opponent.notify_game_over()
                if self.visual:
                    print('\n')
                    print('Draw!')
                break
            else:
                # No point rewarding player until opponent's response
                # and corresponding reward is known
                opponent.reward(0, self.board)
                self.turn_parity *= -1

    def print_board(self):
        row = " {} | {} | {}"
        hr = "\n-----------\n"
        print((row + hr + row + hr + row).format(*self.board))


class TTTPlayer:
    """
    Base class for a player that interacts with the TTTEnv and
    can learn from the results.
    """

    def reset(self):
        pass

    def reward(self, value, achieved_board):
        pass

    def choose_move(self, board):
        pass

    def notify_game_over(self):
        pass

    @staticmethod
    def get_legal_moves(board: list):
        return [i for i in range(9) if board[i] == TTTEnv.chars[0]]


class HPlayer(TTTPlayer):
    """
    Subclass of TTTPlayer for allowing human interaction with the
    environment via the command line.
    """

    def choose_move(self, board):
        print('\n')
        move = int(input("Choose a move from 1-9: ")) - 1
        while move not in self.get_legal_moves(board):
            move = int(input("Invalid move, choose again: ")) - 1
        return move


class QPlayer(TTTPlayer):
    """
    TTTPlayer implementing Q-learning so that the agent can get
    better at playing the game by playing it and observing the
    results.
    """

    def __init__(self, learning_rate=0.5, gamma=0.9, epsilon=0.2):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.qvalues = defaultdict(lambda: defaultdict(lambda: 100.0))
        self.games_played = 0
        self.reset()

    def reset(self):
        self.last_move = None
        self.last_board = [' '] * 9

    def notify_game_over(self):
        self.games_played += 1

    @staticmethod
    def hashable(board: list) -> str:
        return ''.join(board)

    def get_qvalue(self, board: list, action: int):
        return self.qvalues[self.hashable(board)][action]

    def set_qvalue(self, board: list, action: int, value):
        self.qvalues[self.hashable(board)][action] = value

    def get_board_value(self, board: list):
        possible_moves = self.get_legal_moves(board)
        if len(possible_moves) == 0:
            return 0.0
        else:
            return max([self.get_qvalue(board, a) for a in possible_moves])

    def reward(self, value, achieved_board):
        new_qvalue = (1 - self.learning_rate) \
            * self.get_qvalue(self.last_board, self.last_move) \
            + self.learning_rate * (value + self.gamma *
                                    self.get_board_value(achieved_board))
        self.set_qvalue(self.last_board, self.last_move, new_qvalue)

    def choose_move(self, board):
        possible_moves = self.get_legal_moves(board)
        if random() < self.epsilon:
            chosen_move = choice(possible_moves)
        else:
            move_values = [(move, self.get_qvalue(board, move))
                           for move in possible_moves]
            shuffle(move_values)
            chosen_move = max(move_values, key=lambda x: x[1])[0]
        self.last_move = int(chosen_move)
        self.last_board = board.copy()
        return chosen_move
