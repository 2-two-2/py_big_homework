"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns
#q 1  All tests passed
def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    Translation:
    掷骰子函数,投掷指定次数的骰子,并返回结果之和。
    如果结果中出现 1,就算作 Pig out,函数返回 1。

    参数：
    num_rolls: 投掷的骰子个数；必须是一个正整数。
    dice: 一个无参函数,返回一个骰子的点数(1-6之间的整数)。

    返回值：所有骰子点数之和,或者如果有1点,则返回1。
    """
    
    # These assert statements ensure that num_rolls is a positive integer.---->确保 num_rolls 是一个正整数。
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
     # 开始投掷骰子,并判断是否出现 Pig out。
    pig_out = False
    all_dice = [dice() for _ in range(num_rolls)]
    for d in all_dice:
        if d == 1:
            pig_out = True

    # 返回投掷结果之和或者1。
    return 1 if pig_out else sum(all_dice)

# q 2  All tests passed
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.

    Translation:
    模拟一轮游戏,投掷指定次数的骰子,并返回本轮得分。

    参数：
    num_rolls: 投掷的骰子个数。如果是 0,则本轮玩家可以选择得到 Free bacon。
    opponent_score: 对手的总得分
    dice: 表示投掷一个骰子的函数

    返回值：本轮的得分
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    # 如果投掷次数为0，玩家可以选择得到Free bacon
    if num_rolls == 0:
        return max(int(digit) for digit in str(opponent_score)) + 1
    else:
        score = roll_dice(num_rolls, dice) # 调用roll_dice函数，模拟投掷num_rolls个骰子
        # 如果分数是质数，就改为下一个质数
        if is_prime(score):
            score = next_prime(score)
        return score
    
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def next_prime(n):
    i = n + 1
    while not is_prime(i):
        i += 1
    return i   

# Playing a game
# q 3 All tests passed
def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    Translation:
    选择扔骰子的类型：如果 SCORE 和 OPPONENT_SCORE 的和是 7 的倍数,就选择四面骰子。
    否则,选择六面骰子。

    参数：
    score: 自己已有的得分
    opponent_score: 对手已有的得分

    返回值：选择的骰子类型

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == six_sided
    True
    >>> select_dice(0, 0) == four_sided
    True
    """
    "*** YOUR CODE HERE ***"
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.
    给定一个编号为 0 或 1 的玩家,返回另一个玩家的编号。

    参数：
    who: 玩家编号,应为 0 或者 1。

    返回值：另一个玩家的编号,如果 who 为 0,返回 1;如果 who 为 1,返回 0。

    >>> other(0)
    1
    >>> other(1)
    0
    """
    # 如果 who 是 0,返回 1；如果 who 是 1,返回 0。
    return (who + 1) % 2

#q 4
def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    模拟一次游戏并返回两位玩家的最终得分，第一个得分是 Player 0 的得分，第二个得分是 Player 1 的得分。

    策略是一个函数，它接受两个总分数作为参数(当前玩家的得分和对手的得分)，并返回当前玩家本轮要摇动的骰子数。

    参数：
    strategy0: Player 0 的策略函数，先行。
    strategy1: Player 1 的策略函数，后行。
    goal: 游戏的目标得分,默认为GOAL_SCORE。

    返回值：包含两位玩家的最终得分的元组，第一个得分是 Player 0 的得分，第二个得分是 Player 1 的得分。
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # score, opponent_score, dice = 0, 0, six_sided
    "*** YOUR CODE HERE ***"
    score0, score1 = 0, 0
    tmp =0
    while score0 < goal and score1  < goal :
        if who == 0 :
            score0 += take_turn(strategy0(score0,score1),score1,select_dice(score0,score1))
        else :
            score1 += take_turn(strategy1(score0,score1),score0,select_dice(score0,score1))
        who = other(who)
        if score0 == score1 * 2 or score1 == score0 * 2:
            tmp = score0
            score0 = score1
            score1 = tmp
        print('{0:<}{1:>4}'.format(score0,score1))
    return score0,score1
        

#######################
# Phase 2: Strategies #
#######################

# Basic Strategy

BASELINE_NUM_ROLLS = 5
BACON_MARGIN = 8

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
        # return final_strategy(score, opponent_score, six_sided) 

    return strategy

def is_swap(score0, score1):
    """Return whether the tens digit of score0 is the same as the ones digit of score1 and the ones digit of score0 is the same as the tens digit of score1.
     score0: The score of player 0
    score1: The score of player 1
     Returns: True if the tens digit of score0 is the same as the ones digit of score1 and the ones digit of score0 is the same as the tens digit of score1, False otherwise
    """
     # Extract the tens and ones digits from each score
    if score0 > 10 and score1 > 10:
        if str(score0)[-2:] == str(score1)[-2:][::-1]:
            return True
    return False
# Experiments

#q 5 All tests passed
def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def try_and_average(*args):
        res = [fn(*args) for i in range(num_samples)]
        return sum(res)/num_samples
    return try_and_average

#q 6 All tests passed
def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    "*** YOUR CODE HERE ***"
    max_average_score, best_num_rolls = -1, None
    for num_rolls in range(1, 11):
        average_score = make_averaged(roll_dice)(num_rolls, dice)
        print(num_rolls, 'dice scores', average_score, 'on average')
        if average_score > max_average_score:
            max_average_score, best_num_rolls = average_score, num_rolls
    return best_num_rolls

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score, opponent_score = play(strategy0, strategy1)
    if score > opponent_score:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(BASELINE_NUM_ROLLS)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies
# q 7 All tests passed
def bacon_strategy(score, opponent_score):
    """This strategy rolls 0 dice if that gives at least BACON_MARGIN points,
    and rolls BASELINE_NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 0)
    5
    >>> bacon_strategy(70, 50)
    5
    >>> bacon_strategy(50, 70)
    0
    """
    "*** YOUR CODE HERE ***"
    bacon_points = max(opponent_score // 10, opponent_score % 10) + 1
    if bacon_points >= BACON_MARGIN:
        return 0
    return BASELINE_NUM_ROLLS

#q 8 All tests passed
def swap_strategy(score, opponent_score):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.

    >>> swap_strategy(23, 60) # 23 + (1 + max(6, 0)) = 30: Beneficial swap
    0
    >>> swap_strategy(27, 18) # 27 + (1 + max(1, 8)) = 36: Harmful swap
    5
    >>> swap_strategy(50, 80) # (1 + max(8, 0)) = 9: Lots of free bacon
    0
    >>> swap_strategy(12, 12) # Baseline
    5
    """
    "*** YOUR CODE HERE ***"
    if (score + take_turn(0, opponent_score)) * 2 == opponent_score:  #Beneficial swap
        return 0
    elif score + take_turn(0, opponent_score) == opponent_score * 2 or take_turn(0, opponent_score) < BACON_MARGIN:
        return BASELINE_NUM_ROLLS    #Harmful swap or take_turn < 8
    else:
        return 0

    # return 5# Replace this statement

# q 9 All tests passed
def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
    bacon_points = max(opponent_score // 10, opponent_score % 10) + 1
    score += bacon_points
    if is_swap(score, opponent_score):
        if score < opponent_score:
            return 0
        return BASELINE_NUM_ROLLS
    if bacon_points >= BACON_MARGIN:
        return 0
    if is_swap(score + BASELINE_NUM_ROLLS, opponent_score) and opponent_score > score:
        return 0
    return BASELINE_NUM_ROLLS
    # return 5 # Replace this statement


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed.  They use features
#  of Python not yet covered in the course.

def get_int(prompt, min):
    """Return an integer greater than or equal to MIN, given by the user."""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < min:
        print('Please enter an integer greater than or equal to', min)
        choice = input(prompt)
    return int(choice)

def interactive_dice():
    """A dice where the outcomes are provided by the user."""
    return get_int('Result of dice roll: ', 1)

def make_interactive_strategy(player):
    """Return a strategy for which the user provides the number of rolls."""
    prompt = 'Number of rolls for Player {0}: '.format(player)
    def interactive_strategy(score, opp_score):
        if player == 1:
            score, opp_score = opp_score, score
        print(score, 'vs.', opp_score)
        choice = get_int(prompt, 0)
        return choice
    return interactive_strategy

def roll_dice_interactive():
    """Interactively call roll_dice."""
    num_rolls = get_int('Number of rolls: ', 1)
    turn_total = roll_dice(num_rolls, interactive_dice)
    print('Turn total:', turn_total)

def take_turn_interactive():
    """Interactively call take_turn."""
    num_rolls = get_int('Number of rolls: ', 0)
    opp_score = get_int('Opponent score: ', 0)
    turn_total = take_turn(num_rolls, opp_score, interactive_dice)
    print('Turn total:', turn_total)

def play_interactive():
    """Interactively call play."""
    strategy0 = make_interactive_strategy(0)
    strategy1 = make_interactive_strategy(1)
    score, opponent_score = play(strategy0, strategy1)
    print('Final scores:', score, 'to', opponent_score)

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--interactive', '-i', type=str,
                        help='Run interactive tests for the specified question')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.interactive:
        test = args.interactive + '_interactive'
        if test not in globals():
            print('To use the -i option, please choose one of these:')
            print('\troll_dice', '\ttake_turn', '\tplay', sep='\n')
            exit(1)
        try:
            globals()[test]()
        except (KeyboardInterrupt, EOFError):
            print('\nQuitting interactive test')
            exit(0)
    elif args.run_experiments:
        run_experiments()
