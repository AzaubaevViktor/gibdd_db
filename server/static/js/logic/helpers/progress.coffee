class Progress
  constructor: (@el) ->
    @progress = @el.children()
    @el.addClass 'lighten-4'
    @_curColor = ""

  setProgress: (percent) ->
    @progress.css 'width', "#{percent}%"

  setColor: (color) ->
    @el.removeClass @_curColor
    @progress.removeClass @_curColor
    @el.addClass color
    @progress.addClass color
    @_curColor = color


window.progress = new Progress $ '#progress'