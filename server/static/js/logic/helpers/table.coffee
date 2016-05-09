_weekdays = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']
_weekdaysInv = {'Пн':0,'Вт':1,'Ср':2,'Чт':3,'Пт':4,'Сб':5,'Вс':6}

_cmpNum = (a, b) ->
  if a > b then return 1
  else if a < b then return -1
  else return 0

_mod = (a, b) ->
  c = a % b
  return if c < 0 then b + c else c

class Table
  constructor: (@parent, @from, @to, @parts) ->
    @table = tag 'table'
    @parent.append @table
    @rows = []

  addHead: ->
    tr = tag 'tr'
    tr.append tag 'th', '', 'Фамилия', "data-field":'name'
    tr.append tag 'th', '', 'Upd.', 'data-field':'updated'
    tr.append tag 'th', '', 'ДН', 'data-field':'date'
    for hour in [@from..@to-1]
      th = tag 'th', '', hour, 'data-field':"hour_#{hour}", "colspan":@parts
      tr.append th
    thead = tag 'thead', '', tr
    @table.append thead

  makeSortable: (func) ->
    _handlerGenerator = ($th, thi) =>
      $th.click =>
        func thi

    cells = @table.find('thead').children().children()
    for thi in [0..(@to - @from + 2)]
      th = cells[thi]
      $th = $ th
      _handlerGenerator $th, thi

    null

  sortBy: (thi) ->
    if thi == 'now'
      hour = (new Date()).getHours()
      if hour > @to
        hour = @to
      if hour < @from
        hour = @from
      @sortBy hour - @from + 3

    else if 0 <= thi < 3
      @textSort thi
    else
      @schedSort thi
    null

  textSort: (thi) ->
    tb = (@table.find 'tbody')
    trs = tb.children()[..]
    trs = trs.sort (a, b) ->
      order = [thi, 2, 0, 1]
      $cells1 = $ ($ a).children()
      $cells2 = $ ($ b).children()
      for i in order
        c1 = (($ $cells1[i]).attr 'data').trim()
        c2 = (($ $cells2[i]).attr 'data').trim()
        if isNaN(c1)
          cmpResult = c1.localeCompare(c2)
        else
          cmpResult = _cmpNum(c1*1, c2*1)

        if cmpResult != 0
          return cmpResult
      return 0

    for tr in trs
      tb.append(tr)

    null

  schedSort: (thi) ->
    tb = (@table.find 'tbody')
    trs = tb.children()[..]
    [to, from, parts] = [@to, @from, @parts]

    _cells_test = (cells, from, to) ->
      s1 = -1 # Начало первого интервала

      il1 = 0 # Длинна первого интервала

      for i in [from..to]
        c1 = ($ cells[i]).hasClass 'selected'
        if s1 == -1 and !c1
          continue
        if s1 == -1 and c1
          s1 = i
          il1 += 1
          continue
        if s1 > 0 and c1
          il1 += 1
          continue
        if s1 > 0 and !c1
          break
      return [s1, il1]

    sortFunc = (a, b) ->
      $cells1 = $ ($ a).children()
      $cells2 = $ ($ b).children()

      wd1 = (($ $cells1[2]).attr 'data').trim() * 1
      wd2 = (($ $cells2[2]).attr 'data').trim() * 1

      [s1, il1] = _cells_test $cells1, (if wd1 then 3 else (thi-3)*parts + 3), (to - from)*parts + 2
      [s2, il2] = _cells_test $cells2, (if wd2 then 3 else (thi-3)*parts + 3), (to - from)*parts + 2

      if s1 == s2 == -1
        return 0
      if s1 == -1
        return 1
      if s2 == -1
        return -1

      cmpResult = _cmpNum wd1, wd2
      if cmpResult != 0
        return cmpResult

      cmpResult = _cmpNum s1, s2
      if cmpResult != 0
        return cmpResult

      return _cmpNum il2, il1
    trs = trs.sort sortFunc

    for tr in trs
      tb.append(tr)

    null

  selectTd: (td, color) ->
    td.css 'background-color', color
    td.addClass 'selected'

  unselectTd: (td) ->
    td.css 'background-color', 'transparent'
    td.removeClass 'selected'

  _getLine: (title, update_time, wd, times, color, curWeekDay, clickHandler) ->
    tr = tag 'tr'
    cells = []
    lefthead = if needAuthGroup('moderator') then (a '', title, clickHandler) else title
    cells.push tag 'td', '', lefthead, 'data':title
    ddiff = Date.now() - update_time
    cells.push tag 'td', '', dateDiff(ddiff), 'data':ddiff
    cells.push tag 'td', '', _weekdays[wd], 'data': _mod (wd - curWeekDay + 1), 7

    for houri, hour of times
      for parti, part of hour
        td = tag 'td', 'hour', ''
        td.attr 'id', "#{wd}.#{houri}.#{parti}"
        if part
          @selectTd(td, color)
        cells.push td

    tr.append cells

  analyze: (persons) ->
    for person in persons
      @analyzePerson person

  analyzePerson: (person) ->
    firstSymTitle = if person.title then person.title.name[0] else ''
    name = "#{person.name} (#{firstSymTitle})"
    color = person.state.color || 'blue'
    clickHandler = ->
      goto person.name, obj:'person', act:'show', 'id':person.id

    weekdays = {}

    for wd in [0..6]
      hours = weekdays[wd] = {}
      for hour in [@from..@to-1]
        hours[hour] = (false for num in [0..@parts-1])

    # Разбор
    for time in person.times.split(' ')
      [wd, hour, part] = time.split '.'
      if time and @to > hour >= @from
        weekdays[wd][hour][part] = true

    curWeekDay = (new Date()).getDay()
    rows = for index, day of weekdays
      @_getLine(name, person.update_time, index, day, color, curWeekDay, clickHandler)

    @table.append rows


window.Table = Table
