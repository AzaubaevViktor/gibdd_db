class Collection
  constructor: (@parent, @aType=true) ->

    @collection = if @aType then div 'collection' else tag 'ul', 'collection'
    @parent.append @collection

  addLine: (data, handler) ->
    if @aType
      el = a 'collection-item row', data, handler
      @collection.append el
    else
      el = tag 'li', 'collection-item', (div '', data)
      @collection.append el


  remove: () ->
    @collection.remove()
    null


window.Collection = Collection