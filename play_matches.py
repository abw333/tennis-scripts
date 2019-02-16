import random

import tennis

NUM_MATCHES = 100
MATCH_KWARGS = {}

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
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot

  point_win_probs = tuple(scaled_range(start=1, stop=100, scale=0.01))

  axes = matplotlib.pyplot.subplots()[1]

  axes.imshow(
    tuple(
      tuple(
        play_matches(
          first_server_serving_point_win_prob=first_server_serving_point_win_prob,
          first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
          num_matches=NUM_MATCHES,
          match_kwargs=MATCH_KWARGS
        ) for first_returner_serving_point_win_prob in point_win_probs
      ) for first_server_serving_point_win_prob in point_win_probs
    ),
    origin='lower',
    extent=[point_win_probs[0], point_win_probs[-1], point_win_probs[0], point_win_probs[-1]]
  )

  axes.set(
    title=f'P(first server wins match) ({NUM_MATCHES} matches per data point)',
    xlabel='P(first server wins point while returning)',
    ylabel='P(first server wins point while serving)'
  )

  matplotlib.pyplot.show()
