class Collection
  constructor: (@parent, @aType=true, @avatar=false) ->

    @collection = if @aType then div 'collection' else tag 'ul', 'collection'
    @parent.append @collection

  addLine: (data, handler) ->
    if @aType
      el = a 'collection-item row', data, handler
      @collection.append el
    else
      el = tag 'li', 'collection-item', data
      if @avatar
        el.addClass('avatar')
      @collection.append el

  addAvatarLine: (title, about, secondaryContent) ->
    @addLine [
      tag('span', 'title', title),
      p(about),
      div 'secondary-content', secondaryContent
    ]

  remove: () ->
    @collection.remove()
    null


window.Collection = Collection