class Form
  constructor: (id, size, parent) ->
    @form = tag 'form', "col #{size}", '', 'id':id
    @curRow = null
    @dataFields = []
    @main = div 'row', @form
    parent?.append @main
    @addRow()

  addRow: ->
    @curRow = row()
    @form.append @curRow

  addEl: (el) ->
    @curRow.append el

  addInputField: (id, type, size, label, value="") ->
    d = inputField id, type, size, label, value
    @dataFields.push d.find 'input'

    @addEl d
    Materialize.updateTextFields();
    d

  addOptionsField: (id, size, label) ->
    # Возвращает функцию-добалятор опций
    d = div "input-field col #{size}"
    s = tag 'select', '', '', 'id':id
    Materialize.updateTextFields();
    @dataFields.push s

    addOptions = (options, selected) ->
      for v, t of options
        o = tag 'option', '', t, 'value': v
        if 1*v == selected
          o.attr 'selected', ''
        s.append o
      s.material_select()

    l = tag 'label', '', label

    d.append [s, l]

    @addEl d
    return addOptions

  collectData: ->
    result = {}
    for dataField in @dataFields
      result[dataField.attr 'id'] = dataField.val()
    return result


window.Form = Form