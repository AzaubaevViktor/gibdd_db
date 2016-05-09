timers = []
window.delayedSendGenerator = (timerId, params, dataGenerator, successHandler) ->
  # чтобы не загружать частыми eventaми и для того
  # , чтобы selectы успели обновиться
  tmhandler = (event) ->
    progress.setColor 'yellow'
    timer = timers[timerId]
    if timer
      clearTimeout timer

    _this = this

    timers[timerId] = setTimeout ->
      data = dataGenerator(_this)
      AJAXSend params, data, successHandler
      progress.setColor 'green'
    , 1000
  return tmhandler

window.clearSendTimer = (timerId) ->
  timer = timers[timerId]
  if timer
    clearTimeout timer
# TODO: прихуячить сброс таймера