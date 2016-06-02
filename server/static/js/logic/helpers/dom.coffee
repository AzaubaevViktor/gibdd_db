window.tag = (name, cls="", data="", attrs={}) ->
  el = $ "<#{name} class='#{cls}'></#{name}>"
  el.append data
  el.attr(attrs)
  el


window.p = (text) ->
  tag "p", '', data=text

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

window.inputFieldPlaceholder = (id, type, size, label, placeholder, value="") ->
  d = div "input-field col #{size}"
  i = tag 'input', 'validate', '', 'id':id, 'type':type, 'value':value, 'placeholder':placeholder
  l = tag 'label', '', label, 'for':id
  d.append [i, l]
  d

window.inputField = (id, type, size, label, value="") ->
  inputFieldPlaceholder id, type, size, label, '', value

window.valignWrapper = (cls, innerTag) ->
  innerTag.addClass 'valign'
  div "valign-wrapper #{cls}", innerTag