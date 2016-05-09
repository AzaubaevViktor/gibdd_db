class Modal
  constructor: ->
    @modal = $ '#modal'
    @header = @modal.find '#modal-header'
    @text = @modal.find '#modal-text'
    @agree = @modal.find '#modal-agree'

  clear: ->
    @header.empty()
    @text.empty()
    @unsetAgreeHandler()

  show: ->
    @modal.openModal()

  hide: ->
    @modal.closeModal()

  setAgreeHandler: (handler) ->
    @agree.on 'click', ->
      handler()
      false

  unsetAgreeHandler: ->
    @agree.off 'click'


window.modal = new Modal()