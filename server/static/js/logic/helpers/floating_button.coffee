class FloatingButton
  constructor: ->
    @btn = $ '#fb-div'
    @a = $ '#fb-a'
    @btns = $ '#fb-buttons'

  addButton: (icon_name, color, title, handler) ->
    if !@btn?
      return

    @a.removeClass 'disabled'
    i = icon icon_name
    a = tag 'a', "waves-effect btn-floating #{color}", i
    a.click ->
      handler()
      false
    a.dynTooltip(title)
    li = tag 'li', '', a
    @btns.append li

  clear: ->
    if !@btn?
      return

    (@btns.find 'tooltiped').tooltip 'remove'
    @btns.empty()
    @a.addClass "disabled"

window.floatingButton = new FloatingButton()