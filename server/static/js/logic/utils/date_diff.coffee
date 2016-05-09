_dels = [1000, # ms -> s
  60, # s -> min
  60, # min -> hour
  24, # hour -> day
  365/12, # day -> month
  12, # month -> year
]

_sign = ['мс', 'сек.', 'мин.', 'ч.', 'дн.', 'мес.', 'г.']

window.dateDiff = (ms) ->
  prev = ms
  cur = ms
  arr = [ms]
  for i in [0.._dels.length-1]
    cur /= _dels[i]
    if cur < 1
      return "#{prev} #{_sign[i]}"

    prev = cur.toFixed()

  return "#{prev} #{_sign[-1..][0]}"

