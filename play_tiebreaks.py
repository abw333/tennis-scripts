import random

import tennis

NUM_TIEBREAKS = 100
TIEBREAK_KWARGS = {}

def scaled_range(*, start, stop, scale):
  return (i * scale for i in range(start, stop))

def play_tiebreak(
  *,
  first_server_serving_point_win_prob,
  first_returner_serving_point_win_prob,
  tiebreak_kwargs
):
  tiebreak = tennis.Tiebreak(**tiebreak_kwargs)
  while True:
    first_server_point_win_prob = first_server_serving_point_win_prob \
      if tiebreak.first_server_to_serve() \
      else first_returner_serving_point_win_prob
    if tiebreak.point(first_server=random.random() < first_server_point_win_prob) is not None:
      return tiebreak

def play_tiebreaks(
  *,
  first_server_serving_point_win_prob,
  first_returner_serving_point_win_prob,
  num_tiebreaks,
  tiebreak_kwargs
):
  first_server_tiebreaks_won = 0
  for _ in range(num_tiebreaks):
    first_server_tiebreaks_won += play_tiebreak(
      first_server_serving_point_win_prob=first_server_serving_point_win_prob,
      first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
      tiebreak_kwargs=tiebreak_kwargs
    ).winner()
  return first_server_tiebreaks_won / num_tiebreaks

if __name__ == '__main__':
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot

  point_win_probs = tuple(scaled_range(start=1, stop=100, scale=0.01))

  axes = matplotlib.pyplot.subplots()[1]

  axes.imshow(
    tuple(
      tuple(
        play_tiebreaks(
          first_server_serving_point_win_prob=first_server_serving_point_win_prob,
          first_returner_serving_point_win_prob=first_returner_serving_point_win_prob,
          num_tiebreaks=NUM_TIEBREAKS,
          tiebreak_kwargs=TIEBREAK_KWARGS
        ) for first_returner_serving_point_win_prob in point_win_probs
      ) for first_server_serving_point_win_prob in point_win_probs
    ),
    origin='lower',
    extent=[point_win_probs[0], point_win_probs[-1], point_win_probs[0], point_win_probs[-1]]
  )

  axes.set(
    title=f'P(first server wins tiebreak) ({NUM_TIEBREAKS} tiebreaks per data point)',
    xlabel='P(first server wins point while returning)',
    ylabel='P(first server wins point while serving)'
  )

  matplotlib.pyplot.show()
