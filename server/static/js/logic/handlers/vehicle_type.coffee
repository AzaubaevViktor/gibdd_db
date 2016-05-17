initAddEditModal = (VFTs, vehicleType={'features':{}}) ->
  modal.clear()
  modal.header.text 'Изменить название ТС'
  form = new Form 'edit-vehicleType', 's12', modal.text
  form.addInputField 'name', 'text', 's12', 'Название', vehicleType.name
  form.addRow()
  for id, feature of VFTs
    console.log feature
    form.addCheckBox "vft_#{id}", 's6', feature.name, vehicleType.features[id]

  console.log form.collectData()

  modal.setAgreeHandler ->
    data = form.collectData()
    data.id = vehicleType.id
    AJAXSend obj:'vehicleType', act:'add_edit', data, (data) ->
      goto null, obj:'vehicleType', act:'show_all'


generateLine = (params, vehicleType, VFTs) ->
  btnDelete = a 'secondary-content', icon('delete'), ->
    AJAXSend {obj: 'vehicleType', act: 'delete'}, id: vehicleType.id, ->
      goto null, params
  btnEdit = a 'secondary-content', icon('edit'), ->
    initAddEditModal VFTs, vehicleType
    modal.show()
  features = '<br>'
  for id, feature of vehicleType.features
    features += "#{feature.name} (#{featureTypesList[feature.variable_type]})<br>"
  return [tag('b', null, data=vehicleType.name), btnDelete, btnEdit, features]

window.vehicleTypeHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container, false
      VFTs = null
      AJAXLoad obj:'vehicleFeatureType', act:'show_all', (data) ->
        VFTs = data.vehicleFeatureTypes
        null

      AJAXLoad params, (data) ->
        for _id, vehicleType of data.vehicleTypes
          coll.addLine generateLine params, vehicleType, VFTs
          null

      setTitle 'Типы ТС'
      breadcrumb.push 'Типы ТС', params

      floatingButton.addButton 'add', 'green', 'Добавить тип ТС', ->
        initAddEditModal(VFTs)
        modal.show()

