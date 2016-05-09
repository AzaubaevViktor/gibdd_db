window.tag = (name, cls="", data="", attrs={}) ->
  el = $ "<#{name} class='#{cls}'></#{name}>"
  el.append data
  el.attr(attrs)
  el


window.a = (cls, data, handler) ->
  _a = tag 'a', cls, data
  if typeof handler == 'function'
    _a.on 'click', () ->
      handler()
      return false
  return _a


window.div = (cls, data="", attrs={}) ->
  tag 'div', cls, data, attrs


window.row = ->
  tag 'div', 'row', ''


window.icon = (name) ->
  tag 'i', 'material-icons', name


window.inputField = (id, type, size, label, value="") ->
  d = div "input-field col #{size}"
  i = tag 'input', 'validate', '', 'id':id, 'type':type, 'value':value
  l = tag 'label', '', label, 'for':id
  d.append [i, l]
  d


window.valignWrapper = (cls, innerTag) ->
  innerTag.addClass 'valign'
  div "valign-wrapper #{cls}", innerTag