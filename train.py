from tictactoe import TTTEnv, QPlayer, HPlayer
import json
import click


@click.command()
@click.option('-n', default=500000, show_default=True)
@click.option('--play', is_flag=True)
@click.option('--store_optimal_moves', is_flag=True)
@click.option('--moves_target', default='./js/ai_moves.js')
def train(n, play, store_optimal_moves, moves_target):
    """
    Train the AI to play Tic Tac Toe by making two AI agents
    play against each other. Optionally let one of the agents
    play against a human when it is trained.
    """

    # Initialize two Q-learning-based agents
    q_player_1 = QPlayer()
    q_player_2 = QPlayer()

    # Make them play against themselves
    print("WOPR is playing Tic Tac Toe against itself...")
    for i in range(n):
        if i % (n/10) == 0:
            print(f"Game {i}...")
        game = TTTEnv(q_player_1, q_player_2)
        game.play_game()

    # Output the moves learned by the AI
    if store_optimal_moves:
        print(f"Saving optimal moves learned after playing {n} games...")
        optimal_moves = {key: max(dict(val), key=dict(val).get)
                         for key, val in q_player_2.qvalues.items()}

        ai_moves_js = f"""
/*
 * Tic Tac Toe - AI Moves
 *
 * Optimal (approximately) moves for Tic Tac Toe
 * learned using reinforcement learning.
 * The AI played {n} moves against itself to obtain
 * this set of moves.
 *
 * @author: Marco Tompitak
 */

var ai_moves = JSON.parse(`
{json.dumps(optimal_moves, indent=2)}`);
        """

        with open(moves_target, "w") as f:
            f.write(ai_moves_js)

    while play:
        print(f"AI has been trained for {n} rounds, starting human game...")

        # Initialize a human player
        h_player = HPlayer()
        print("You are playing as X")
        print("You are playing against a QPlayer that has played %d games" %
              q_player_2.games_played)
        print('\n')

        # Play a game
        game = TTTEnv(h_player, q_player_2, visual=True)
        game.play_game()

        # Loop if the user wants to play again
        play = input("The only winning move is not to play. "
                     "Play again? y/n: ")[0] == 'y'


if __name__ == '__main__':
    train()
