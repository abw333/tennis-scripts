import random
import time

import tennis

NUM_MATCHES = 100
MATCH_KWARGS = {}
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
    ).winner()
  return first_server_matches_won / num_matches

if __name__ == '__main__':
  start = time.time()

  point_win_probs = tuple(scaled_range(start=1, stop=100, scale=0.01))

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
          f'Elapsed time: {elapsed:.0f}s'
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
          match_kwargs=MATCH_KWARGS
        )
        match_win_probs_cache[_cache_key(
          float1=first_server_serving_point_win_prob,
          float2=first_returner_serving_point_win_prob
        )] = match_win_prob
      match_win_probs_col.append(match_win_prob)
    match_win_probs.append(match_win_probs_col)

  elapsed = time.time() - start
  print(f'\033[KDone playing matches! Elapsed time: {elapsed:.0f}s')

  if PLOT:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot

    axes = matplotlib.pyplot.subplots()[1]

    axes.imshow(
      match_win_probs,
      origin='lower',
      extent=[point_win_probs[0], point_win_probs[-1], point_win_probs[0], point_win_probs[-1]]
    )

    axes.set(
      title=f'P(first server wins match) ({NUM_MATCHES} matches per data point)',
      xlabel='P(first server wins point while returning)',
      ylabel='P(first server wins point while serving)'
    )

    matplotlib.pyplot.show()
