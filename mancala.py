import cs210_utils
from games import Game

class MancalaGame(Game):
    def __init__(self):
        self.initial = [[4,4,4,4,4,4,0,4,4,4,4,4,4,0], 0]

    def legal_moves(self, state):
        """Return a list of the allowable moves
        at this point. A state represents the number
        of stones in each pit on the board.

        >>> mg = MancalaGame()
        >>> state = [[4,4,4,4,4,4,0,4,4,4,4,4,4,0], 0]
        >>> MancalaGame.legal_moves(mg, state)
        [0, 1, 2, 3, 4, 5]

        >>> state = [[4,4,4,4,4,4,0,4,0,5,5,5,5,0], 1]
        >>> MancalaGame.legal_moves(mg, state)
        [0, 2, 3, 4, 5]

        >>> state = [[0,0,0,0,0,0,0,0,0,0,0,1,0,0], 1]
        >>> MancalaGame.legal_moves(mg, state)
        [4]
        """
        moves = []
        board, turn = state
        if turn == 0:
            for i in range(6):
                if board[i] > 0:
                    moves.append(i)
        else:
            for i in range(6):
                if board[7+i] > 0:
                    moves.append(i)
        return moves

    def make_move(self, move, state):
        """Return the state that results from making
        a move from a state. For Mancala, a move is
        an integer in the range 0 to 5, inclusive.

        Testing whether basic moves work.
        >>> mg = MancalaGame()
        >>> state = [[4,4,4,4,4,4,0,4,4,4,4,4,4,0], 0]
        >>> state = MancalaGame.make_move(mg, 0, state)
        >>> state
        [[0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0], 1]

        Testing whether wrap-around works.
        >>> state = MancalaGame.make_move(mg, 5, state)
        >>> state
        [[1, 6, 6, 5, 5, 4, 0, 4, 4, 4, 4, 4, 0, 1], 0]

        Testing whether turn is maintained after landing in players Mancala.
        >>> state = [[4,4,4,4,4,4,0,4,4,4,4,4,4,0], 0]
        >>> state = MancalaGame.make_move(mg, 2, state)
        >>> state
        [[4, 4, 0, 5, 5, 5, 1, 4, 4, 4, 4, 4, 4, 0], 0]

        Testing whether capturing on empty works for player 0.
        >>> state = [[4,4,4,4,0,5,1,0,6,5,5,5,5,0], 0]
        >>> state = MancalaGame.make_move(mg, 0, state)
        >>> state
        [[0, 5, 5, 5, 0, 5, 8, 0, 0, 5, 5, 5, 5, 0], 1]

        Testing whether capturing on empty works for player 1.
        >>> state = [[0,6,0,0,0,0,0,4,0,0,0,0,0,0], 1]
        >>> state = MancalaGame.make_move(mg, 0, state)
        >>> state
        [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 7], 0]

        Testing whether opponent's Mancala is skipped and that full cycle succeeds.
        >>> state = [[0,0,0,0,0,15,0,0,0,0,0,0,0,0], 0]
        >>> state = MancalaGame.make_move(mg, 5, state)
        >>> state
        [[1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 0], 1]
        """
        board, turn = state
        board = board.copy()

        if turn == 0:
            stones = board[move]
            if stones == 0:
                return [board, turn]
            board[move] = 0
            i = move + 1
            while stones > 0:
                if i == 13:
                    i = 0
                else:
                    stones -= 1
                    board[i] += 1
                    if stones == 0 and i != 6:
                        if i != 6:
                            turn ^= 1
                        if i < 6 and board[i] == 1 and board[12 - i] != 0:
                            board[6] += board[i] + board[12 - i]
                            board[12 - i] = 0
                            board[i] = 0
                    i += 1
        else:
            move += 7
            stones = board[move]
            if stones == 0:
                return [board, turn]
            board[move] = 0
            i = move + 1
            while stones > 0:
                if i == 6:
                    i += 1
                elif i == 14:
                    i = 0
                else:
                    board[i] += 1
                    stones -= 1
                    if stones == 0:
                        if i != 13:
                            turn ^= 1
                        if 6 < i < 13 and board[i] == 1 and board[12 - i] != 0:
                            board[13] += board[i] + board[12 - i]
                            board[12 - i] = 0
                            board[i] = 0
                    i += 1
        return [board, turn]

    def utility(self, state, player):
        """Return the value of this final state to player."""
        board, turn = state
        if player == 0:
            if board[6] - board[13] > 0:
                return 1
            elif board[6] - board[13] < 0:
                return -1
            else:
                return 0
        else:
            if board[13] - board[6] > 0:
                return 1
            elif board[13] - board[6] < 0:
                return -1
            else:
                return 0

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        board, turn = state
        bot_empty = True
        top_empty = True
        for i in range(6):
            if board[i] != 0:
                bot_empty = False
            if board[7+i] != 0:
                top_empty = False
        return bot_empty or top_empty

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        board, turn = state
        return turn

    def display(self, state):
        """Print or otherwise display the state."""
        board, turn = state
        bot = board[:6]
        bot_man = board[6]
        top = list(reversed(board[7:13]))
        top_man = board[13]
        print('{:^30}'.format(str(top)))
        print(str(top_man) + '{:^28}'.format("") + str(bot_man))
        print('{:^30}'.format(str(bot)))
        print('{:-^32}'.format(""))

    def eval_fn(self, state):
        """Takes a game and a state and returns a value for that state"""
        board, turn = state
        return board[13] - board[6]

if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()
