class BreadCrumb
  constructor: ->
    @div = $ '#breadcrumb'
    @items = []
    @_push 'БД ГИБДД', obj:'schedule', act:'show_all'

  _push: (name, params) ->
    item = a 'breadcrumb', name, ->
      goto name, params
    @div.append item
    item

  push: (name, params) ->
    @items.push @_push name, params

  popAll: ->
    for item in @items
      item.remove()
    @items = []


($ document).ready ->
  window.breadcrumb = new BreadCrumb()