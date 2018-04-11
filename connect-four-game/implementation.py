"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function


INFINITY = float("inf")
NEG_INFINITY = float("-inf")


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

STUDENT_ID = 20739061
AGENT_NAME = 'Masijia Qiu'
COMPETE = True

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.


def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    # qmsj
    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 2000 - board.num_tokens_on_board()
    elif board.longest_chain(board.get_other_player_id()) == 4:
        score = -2000 - board.num_tokens_on_board()
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
    return score
    # raise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal,
                      verbose=True):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.
     
     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.
    
     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.
    
     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """
    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -alphabeta_find_board_value(NEG_INFINITY, INFINITY,
                                            new_board, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        
        if best_val is None or val > best_val[0]:
            best_val = (val, move, new_board)
            
    # if verbose:
    #     print("ALPHABETA: Decided on column {} with rating {}".format(best_val[1], best_val[0]))

    return best_val[1]
    # raise NotImplementedError



def alphabeta_find_board_value(alpha, beta, board, depth, eval_fn,  
                                get_next_moves_fn=get_all_next_moves, 
                                is_terminal_fn=is_terminal):

    if is_terminal_fn(depth, board):
        return eval_fn(board)

    for move, new_board in get_next_moves_fn(board):
        
        child_value = alphabeta_find_board_value(-beta, -alpha, new_board, depth-1, eval_fn,  get_next_moves_fn, is_terminal_fn)
        
        if alpha < -child_value:
            alpha = -child_value
        # print(new_board.__str__(), alpha, beta)
        if alpha >= beta:
            # print(new_board.__str__(), alpha)
            return alpha
    return alpha



# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=6, eval_fn=focused_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

# def basic_evaluate(board):
#     """
#     The original focused-evaluate function.
#     """
#     if board.is_game_over():
#         # If the game has been won, we know that it must have been
#         # won or ended by the previous move.
#         # The previous move was made by our opponent.
#         # Therefore, we can't have won, so return -1000.
#         # (note that this causes a tie to be treated like a loss)
#         score = -1000
#     else:
#         score = board.longest_chain(board.get_current_player_id()) * 10
#         # Prefer having your pieces in the center of the board.
#         for row in range(6):
#             for col in range(7):
#                 if board.get_cell(row, col) == board.get_current_player_id():
#                     score -= abs(3-col)
#                 elif board.get_cell(row, col) == board.get_other_player_id():
#                     score += abs(3-col)

#     return score
def hid_better_evaluate(board):
    score = 0
    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 2000 - board.num_tokens_on_board()
    elif board.longest_chain(board.get_other_player_id()) == 4:
        score = -2000 + board.num_tokens_on_board()
    else:
        current_player = board.get_current_player_id()
        other_player = board.get_other_player_id()
        for row in range(0,3):
            for col in range(0, 4):
                score += max([get_chain_len(i, board, row, col, current_player) for i in range(0,3)])**2
                score -= max([get_chain_len(i, board, row, col, other_player) for i in range(0,3)])**2
    return score

def get_chain_len(chain_type, board, row, col, player):
    count = 0
    for i in range(0,3):
        if chain_type == 0 and board.get_cell(row, col+i) == player:
            count += 1
        elif chain_type == 1 and board.get_cell(row+i, col) == player:
            count += 1
        elif chain_type == 2 and board.get_cell(row+i, col+i) == player:
            count += 1
    return count

def get_row_value(board, col, player):
    if board.get_height_of_column(col)>5:
        return 1
    row = board.get_height_of_column(col) + 1
    if board.get_top_elt_in_column(col) == player:
        return board._max_length_from_cell(row, col)
    else:
        return 1

def better_evaluate(board):
    score = 0
    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 2000 - board.num_tokens_on_board()
    elif board.longest_chain(board.get_other_player_id()) == 4:
        score = -2000 + board.num_tokens_on_board()
    else:

        score += board.longest_chain(board.get_current_player_id()) **2
        

        for col in range(0, 7):
            if board.get_height_of_column(col) > 5:
                continue
            row = board.get_height_of_column(col) + 1

            
            if board.get_top_elt_in_column(col) == board.get_current_player_id():
                score += board._max_length_from_cell(row, col) **2
            else:
                score -= board._max_length_from_cell(row, col) **2
        
    return score

    # raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
