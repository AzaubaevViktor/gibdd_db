class DynamicSchedule extends Schedule
  dynamic: ->
    if current_browser[0] == 'firefox'
      Materialize.toast "<b>Firefox</b>?<br>
На этом говне кое-что не работает,<br>
поэтому править таблицу тут нельзя.<br>
Пользуйтесь <a href='https://www.google.com/chrome/'>Google Chrome</a>", 10000
      return

    tds = @table.find('td')
    _this = @

    # Для отмены выделения
    EHR.registry @table, 'mousedown', (event) ->
      return false

    # Меняется ячейка, если мышь ПОЯВЛЯЕТСЯ над ней
    EHR.registry tds, 'mouseover', (event) ->
      console.log event.which, event.keyCode
      if event.which == 1
        _this.change $ this

    # Чтобы менялась ячейка, на которой нажата кнопка
    EHR.registry tds, 'mousedown', (event) ->
      if event.which == 1
        _this.change $ this


window.DynamicSchedule = DynamicSchedule