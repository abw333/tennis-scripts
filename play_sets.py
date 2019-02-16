import random

import tennis

NUM_SETS = 100
SET_KWARGS = {}

def scaled_range(*, start, stop, scale):
  return (i * scale for i in range(start, stop))

def play_set(
  *,
  first_server_serving_point_win_prob,
  first_returner_serving_point_win_prob,
  set_kwargs
):
  zet = tennis.Set(**set_kwargs)
  while True:
    first_server_point_win_prob = first_server_serving_point_win_prob \
      if zet.first_server_to_serve() \
      else first_returner_serving_point_win_prob
    if zet.point(first_server=random.random() < first_server_point_win_prob) is not None:
      return zet

def play_sets(
  *,
  first_server_serving_point_win_prob,
  first_returner_serving_point_win_prob,
  num_sets,
  set_kwargs
):
  first_server_sets_won = 0
  for _ in range(num_sets):
    first_server_sets_won += play_set(
      first_server_serving_point_win_prob=first_server_serving_point_win_prob,
      first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
      set_kwargs=set_kwargs
    ).winner()
  return first_server_sets_won / num_sets

if __name__ == '__main__':
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot

  point_win_probs = tuple(scaled_range(start=1, stop=100, scale=0.01))

  axes = matplotlib.pyplot.subplots()[1]

  axes.imshow(
    tuple(
      tuple(
        play_sets(
          first_server_serving_point_win_prob=first_server_serving_point_win_prob,
          first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
          num_sets=NUM_SETS,
          set_kwargs=SET_KWARGS
        ) for first_returner_serving_point_win_prob in point_win_probs
      ) for first_server_serving_point_win_prob in point_win_probs
    ),
    origin='lower',
    extent=[point_win_probs[0], point_win_probs[-1], point_win_probs[0], point_win_probs[-1]]
  )

  axes.set(
    title=f'P(first server wins set) ({NUM_SETS} sets per data point)',
    xlabel='P(first server wins point while returning)',
    ylabel='P(first server wins point while serving)'
  )

  matplotlib.pyplot.show()
