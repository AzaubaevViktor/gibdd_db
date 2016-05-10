initAddModal = ->
  modal.header.text 'Создать новый тип ТС'
  form = new Form 'new-vehicleType', 's12', modal.text
  form.addInputField 'name', 'text', 's12', 'Название'
  modal.setAgreeHandler ->
    data = form.collectData()
    AJAXSend obj:'vehicleType', act:'add', data, (data) ->
      goto null, obj:'vehicleType', act:'show_all'

window.vehicleTypeHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container, false
      AJAXLoad params, (data) ->
        for vehicleType in data.vehicleTypes
          coll.addLine vehicleType.name, null

      setTitle 'Типы ТС'
      breadcrumb.push 'Типы ТС', params
      initAddModal()


      floatingButton.addButton 'add', 'green', 'Добавить тип ТС', ->
        modal.show()

