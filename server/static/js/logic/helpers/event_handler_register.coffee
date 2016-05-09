class EventHandlerRegister
  # Следит за пользовательскими событиями
  constructor: ->
    @events = []

  registry: (el, ev, handler) ->
    @events.push([el, ev, handler])
    el.on ev, handler

  unregistry: ->
    for [el, ev, handler] in @events
      el.off ev, handler

window.EHR = new EventHandlerRegister()
