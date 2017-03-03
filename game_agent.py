"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

class InvalidMethod(Exception):
    """
    If you try to pass a method that is not minimax or alphabeta.
    """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: tune theta1 and theta2 to weights that maximze winning. For now, just return 1
    # We could use gradient descent to find values for theta that maximize wins.
    # Ahother option is to weight theta1 and theta2 based on how close you are to the endgame.
    # Nash equilibrium?
    theta0 = 0.0
    theta1 = 1.0
    theta2 = -1.0
    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return theta0 + (theta1 * my_moves) + (theta2 * opponent_moves)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

        self.current_depth = 0

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        self.current_depth = 0
        move = (-1,-1)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method == 'minimax':
                _, move = self.minimax(game, self.search_depth, True)
            elif self.method == 'alphabeta':
                _, move = self.alphabeta(game, 3)
            else:
                raise InvalidMethod()

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves()
        if len(legal_moves) <= 0:
            return (self.score(game, game.active_player), (-1, -1))

        # get score for active player's opponent position since game has been advanced
        if depth == 0: # return best move from the board
            score_player = game.__player_2__ if maximizing_player else game.__player_1__
            score_move = (self.score(game, score_player),
                          game.get_player_location(score_player))
            return score_move

        scores = []
        for move in legal_moves:
            new_game = game.forecast_move(move)
            scores.append(self.minimax(new_game, depth-1, False))
        if maximizing_player:
            best_value = max(scores)
        else:
            best_value = min(scores)

        print('scores are {}\nmoving to {} because score is {}. level {}\n\n'
              .format(scores, best_value[1], best_value[0], depth))
        return best_value


        # optimum_move = (0, (-1, -1))
        # if self.iterative:
        #     print("PERFORMING ITERATIVE DEEPENING")
        #     for depth_index in range(1, depth+1):
        #         scores = [(self.score(game.forecast_move(move), game.active_player), move)
        #                   for move in legal_moves]
        #         if maximizing_player:
        #             print("pick max from {}".format(scores))
        #             optimum_move = max(scores)
        #         else:
        #             print("pick min from {}".format(scores))
        #             optimum_move = min(scores)
        #         print("Optimum move at level {} is {}".format(depth_index, optimum_move))
        #         # self.minimax(game.forecast_move(optimum_move), depth+1, not maximizing_player)

        #     return optimum_move
        # else:
        #     # 1. Walk down to the provided depth
        #     # 2. Recursively 
        #     new_game = game
        #     for index in range(depth):
        #         for move in legal_moves:
        #             new_game = new_game.forecast_move(move)
        #             score = self.score(new_game, game.active_player)
        #             boards.append((score, new_game)
        #         if maximizing_player and ((index % 2) == 0):
        #             print("pick max from {}".format(scores))
        #             optimum_board = max(scores)
        #         else:
        #             print("pick min from {}".format(scores))
        #             optimum_board = min(scores)
        #         legal_moves = optimum_board.get_legal_moves()
        #     return self.minimax(optimum_board, depth-1, not maximizing_player)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        score = 0.0
        move = (-1, -1)

        return (score, move)
