class Schedule extends Table
  analyzePerson: (person) ->
    @person = person
    @color = person.state.color || 'blue'
    super person

  selectTd: (td, color) ->
    super td, @color

  change: (td) ->
    if td.hasClass 'hour'
      if td.hasClass 'selected'
        @unselectTd td
      else
        @selectTd td

  collectData: ->
    result = update_time: Date.now(), times: ""

    for td in @table.find('td.hour')
      td = $ td
      if td.hasClass 'selected'
        result.times += "#{td.attr 'id'} "

    return result


window.Schedule = Schedule