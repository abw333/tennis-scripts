import random

import tennis

NUM_GAMES = 5000
#GAME_KWARGS = ({},)
#GAME_KWARGS = ({'deciding_point': False}, {'deciding_point': True})
GAME_KWARGS = (
  {'server_points': 0, 'returner_points': 0},
  {'server_points': 0, 'returner_points': 1},
  {'server_points': 0, 'returner_points': 2},
  {'server_points': 0, 'returner_points': 3},
  {'server_points': 1, 'returner_points': 0},
  {'server_points': 1, 'returner_points': 1},
  {'server_points': 1, 'returner_points': 2},
  {'server_points': 1, 'returner_points': 3},
  {'server_points': 2, 'returner_points': 0},
  {'server_points': 2, 'returner_points': 1},
  {'server_points': 2, 'returner_points': 2},
  {'server_points': 2, 'returner_points': 3},
  {'server_points': 3, 'returner_points': 0},
  {'server_points': 3, 'returner_points': 1},
  {'server_points': 3, 'returner_points': 2},
  {'server_points': 3, 'returner_points': 3}
)

def with_defaults(game_kwargs):
  game_kwargs.setdefault('server_points', 0)
  game_kwargs.setdefault('returner_points', 0)
  game_kwargs.setdefault('deciding_point', False)
  return game_kwargs

def scaled_range(*, start, stop, scale):
  return (i * scale for i in range(start, stop))

def play_game(*, server_point_win_prob, game_kwargs):
  game = tennis.Game(**game_kwargs)
  while True:
    if game.point(first_server=random.random() < server_point_win_prob) is not None:
      return game

def play_games(*, server_point_win_prob, num_games, game_kwargs):
  server_games_won = 0
  for _ in range(num_games):
    server_games_won += play_game(
      server_point_win_prob=server_point_win_prob,
      game_kwargs=game_kwargs
    ).winner()
  return server_games_won / num_games

if __name__ == '__main__':
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot

  GAME_KWARGS = tuple(with_defaults(game_kwargs) for game_kwargs in GAME_KWARGS)

  server_point_win_probs = tuple(scaled_range(start=0, stop=101, scale=0.01))

  axes = matplotlib.pyplot.subplots()[1]

  for game_kwargs in GAME_KWARGS:
    axes.plot(
      server_point_win_probs,
      [play_games(server_point_win_prob=p, num_games=NUM_GAMES, game_kwargs=game_kwargs)
        for p in server_point_win_probs],
      marker='o'
    )

  axes.set(
    title=f'{NUM_GAMES} games per data point',
    xlabel='P(server wins point)',
    ylabel='P(server wins game)'
  )

  axes.legend(GAME_KWARGS)

  axes.grid()

  matplotlib.pyplot.show()
