window.featureTypesList = ['Дата', 'Строка', 'Число', 'Дробное число']

initModal = (vehicleFeatureType={}) ->
  modal.clear()
  modal.header.text 'Создать новый тип параметров ТС'
  form = new Form 'new-vehicleFeatureType', 's12', modal.text
  form.addInputField 'name', 'text', 's6', 'Название', vehicleFeatureType.name
  addOptions = form.addOptionsField 'variable_type', 's6', 'Тип параметра'
  addOptions featureTypesList, vehicleFeatureType.variable_type ? 2
  modal.setAgreeHandler ->
    data = form.collectData()
    data.id = vehicleFeatureType.id
    AJAXSend obj:'vehicleFeatureType', act:'add_edit', data, (data) ->
      goto null, obj:'vehicleFeatureType', act:'show_all'
  null


generateLine = (vehicleFeatureType) ->
  btnDelete = a 'secondary-content', icon('delete'), ->
    AJAXSend {obj: 'vehicleFeatureType', act: 'delete'}, id: vehicleFeatureType.id, ->
      goto null, obj:'vehicleFeatureType'
  btnEdit = a 'secondary-content', icon('edit'), ->
    initModal vehicleFeatureType
    modal.show()
  return [
    "#{vehicleFeatureType.name} (#{featureTypesList[vehicleFeatureType.variable_type]})",
    btnDelete,
    btnEdit]

window.vehicleFeatureTypeHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container, false
      AJAXLoad params, (data) ->
        for vehicleFeatureType in data.vehicleFeatureTypes
          coll.addLine generateLine vehicleFeatureType

      setTitle 'Типы параметров ТС'
      breadcrumb.push 'Типы параметров ТС', params

      floatingButton.addButton 'add', 'green', 'Добавить тип параметров ТС', ->
        initModal()
        modal.show()