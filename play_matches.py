import random
import time

import tennis

NUM_MATCHES = 10

MATCH_KWARGS = {
  'ATP Tour': {
    'target_sets': 2,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 6,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 6,
    'final_set_tiebreak_points': 7
  },
  'Australian Open': {
    'target_sets': 3,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 6,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 6,
    'final_set_tiebreak_points': 10
  },
  'French Open': {
    'target_sets': 3,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 6,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': None,
    'final_set_tiebreak_points': None
  },
  'Wimbledon': {
    'target_sets': 3,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 6,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 12,
    'final_set_tiebreak_points': 7
  },
  'US Open': {
    'target_sets': 3,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 6,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 6,
    'final_set_tiebreak_points': 7
  },
  'Next Gen Finals': {
    'target_sets': 3,
    'target_games': 4,
    'deciding_point': True,
    'tiebreak_games': 3,
    'tiebreak_points': 7,
    'final_set_target_games': 4,
    'final_set_deciding_point': True,
    'final_set_tiebreak_games': 3,
    'final_set_tiebreak_points': 7
  },
  'Doubles': {
    'target_sets': 2,
    'target_games': 6,
    'deciding_point': True,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 0,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 0,
    'final_set_tiebreak_points': 10
  },
  'Tiebreak': {
    'target_sets': 1,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 0,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 0,
    'final_set_tiebreak_points': 7
  },
  'Super Tiebreak': {
    'target_sets': 1,
    'target_games': 6,
    'deciding_point': False,
    'tiebreak_games': 6,
    'tiebreak_points': 7,
    'final_set_target_games': 0,
    'final_set_deciding_point': False,
    'final_set_tiebreak_games': 0,
    'final_set_tiebreak_points': 10
  }
}
MATCH_KWARGS_KEY = 'ATP Tour'

PLOT = True

def scaled_range(*, start, stop, scale):
  return (i * scale for i in range(start, stop))

def play_match(
  *,
  first_server_serving_point_win_prob,
  first_returner_serving_point_win_prob,
  match_kwargs
):
  match = tennis.Match(**match_kwargs)
  while True:
    first_server_point_win_prob = first_server_serving_point_win_prob \
      if match.first_server_to_serve() \
      else first_returner_serving_point_win_prob
    if match.point(first_server=random.random() < first_server_point_win_prob) is not None:
      return match

def _cache_key(*, float1, float2):
  return (f'{float1:.4f}', f'{float2:.4f}')

def play_matches(
  *,
  first_server_serving_point_win_prob,
  first_returner_serving_point_win_prob,
  num_matches,
  match_kwargs
):
  first_server_matches_won = 0
  for _ in range(num_matches):
    first_server_matches_won += play_match(
      first_server_serving_point_win_prob=first_server_serving_point_win_prob,
      first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
      match_kwargs=match_kwargs
    ).winner
  return first_server_matches_won / num_matches

if __name__ == '__main__':
  print(f'Using {MATCH_KWARGS_KEY} scoring rules')
  start = time.time()

  point_win_probs = tuple(scaled_range(start=10, stop=91, scale=0.01))

  match_win_probs_cache = {}
  match_win_probs = []
  for first_server_serving_point_win_prob in point_win_probs:
    match_win_probs_col = []
    for first_returner_serving_point_win_prob in point_win_probs:
      elapsed = time.time() - start
      print(
        (
          f'Playing {NUM_MATCHES} matches with '
          f'first_server_serving_point_win_prob={first_server_serving_point_win_prob:.2f} and '
          f'first_returner_serving_point_win_prob={first_returner_serving_point_win_prob:.2f}. '
          f'Elapsed time: {elapsed:.2f}s'
        ),
        end='\r'
      )
      if _cache_key(
        float1=1 - first_server_serving_point_win_prob,
        float2=1 - first_returner_serving_point_win_prob
      ) in match_win_probs_cache:
        match_win_prob = 1 - match_win_probs_cache[_cache_key(
          float1=1 - first_server_serving_point_win_prob,
          float2=1 - first_returner_serving_point_win_prob
        )]
      else:
        match_win_prob = play_matches(
          first_server_serving_point_win_prob=first_server_serving_point_win_prob,
          first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
          num_matches=NUM_MATCHES,
          match_kwargs=MATCH_KWARGS[MATCH_KWARGS_KEY]
        )
        match_win_probs_cache[_cache_key(
          float1=first_server_serving_point_win_prob,
          float2=first_returner_serving_point_win_prob
        )] = match_win_prob
      match_win_probs_col.append(match_win_prob)
    match_win_probs.append(match_win_probs_col)

  elapsed = time.time() - start
  print(f'\033[KDone playing matches! Elapsed time: {elapsed:.2f}s')

  if PLOT:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot

    axes = matplotlib.pyplot.subplots(figsize=(8, 8))[1]

    axes.imshow(
      match_win_probs,
      origin='lower',
      extent=[point_win_probs[0], point_win_probs[-1], point_win_probs[0], point_win_probs[-1]]
    )

    axes.set(
      title=(
        f'P(first server wins match) '
        f'({NUM_MATCHES} matches with {MATCH_KWARGS_KEY} scoring rules per data point)'
      ),
      xlabel='P(first server wins point while returning)',
      ylabel='P(first server wins point while serving)'
    )

    matplotlib.pyplot.savefig(f'{MATCH_KWARGS_KEY}-{NUM_MATCHES}.png')
    matplotlib.pyplot.show()
