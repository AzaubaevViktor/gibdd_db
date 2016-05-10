initAddModal = ->
  modal.clear()
  modal.header.text 'Создать новый тип ТС'
  form = new Form 'new-vehicleType', 's12', modal.text
  form.addInputField 'name', 'text', 's12', 'Название'
  modal.setAgreeHandler ->
    data = form.collectData()
    AJAXSend obj:'vehicleType', act:'add', data, (data) ->
      goto null, obj:'vehicleType', act:'show_all'

initEditModal = (vehicleType) ->
  modal.clear()
  modal.header.text 'Изменить название ТС'
  form = new Form 'edit-vehicleType', 's12', modal.text
  form.addInputField 'name', 'text', 's12', 'Название', vehicleType.name
  modal.setAgreeHandler ->
    data = form.collectData()
    data.id = vehicleType.id
    AJAXSend obj:'vehicleType', act:'edit', data, (data) ->
      goto null, obj:'vehicleType', act:'show_all'


generateLine = (params, vehicleType) ->
  btnDelete = a 'secondary-content', icon('delete'), ->
    AJAXSend {obj: 'vehicleType', act: 'delete'}, id: vehicleType.id, ->
      goto null, params
  btnEdit = a 'secondary-content', icon('edit'), ->
    initEditModal vehicleType
    modal.show()
  return [vehicleType.name, btnDelete, btnEdit]

window.vehicleTypeHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container, false
      AJAXLoad params, (data) ->
        for vehicleType in data.vehicleTypes
          coll.addLine generateLine params, vehicleType
          null

      setTitle 'Типы ТС'
      breadcrumb.push 'Типы ТС', params

      floatingButton.addButton 'add', 'green', 'Добавить тип ТС', ->
        initAddModal()
        modal.show()

